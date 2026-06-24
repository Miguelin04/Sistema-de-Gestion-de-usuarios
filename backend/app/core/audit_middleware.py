# Autor: Antigravity
# Fecha: 24/06/2026
# Version: 2.0

import time
import json
import socket
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from confluent_kafka import Producer
from jose import jwt
from app.core.config import settings
from app.database.session import SessionLocal
from app.models.auditoria import Auditoria

# Configuración básica de Kafka
conf = {
    'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
    'client.id': socket.gethostname()
}

try:
    producer = Producer(conf)
except Exception as e:
    print(f"Error inicializando Kafka Producer en middleware: {e}")
    producer = None

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

async def get_body(request: Request) -> bytes:
    """Lee el cuerpo de la petición de forma segura sin bloquear las lecturas posteriores."""
    body = await request.body()
    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}
    request._receive = receive
    return body

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Determinar si la ruta y método son de interés para la auditoría
        path = request.url.path
        method = request.method
        
        is_login = path.endswith("/auth/login") or path.endswith("/auth/login-google")
        is_register = path.endswith("/auth/registro") or path.endswith("/auth/google-register") or path.endswith("/auth/registro-hibrido")
        is_user_mgmt = "/usuarios" in path

        # Auditar inicios de sesión, registros y cualquier mutación (POST, PUT, DELETE)
        is_audit_target = is_login or is_register or is_user_mgmt or (method in ["POST", "PUT", "DELETE"])

        if not is_audit_target:
            return await call_next(request)

        # 2. Interceptar el cuerpo del request antes de procesar para obtener el correo si es anónimo
        user_email = "Anónimo"
        if is_login or is_register:
            try:
                body_bytes = await get_body(request)
                if body_bytes:
                    body_data = json.loads(body_bytes.decode('utf-8'))
                    user_email = body_data.get("correo") or body_data.get("email") or "Anónimo"
            except Exception:
                pass

        # 3. Procesar la petición
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000

        # 4. Si es un usuario autenticado (JWT Bearer Token), obtener su correo electrónico
        if user_email == "Anónimo":
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                try:
                    token = auth_header.split(" ")[1]
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                    user_email = payload.get("sub") or "Anónimo"
                except Exception:
                    pass

        # 5. Clasificar el evento para la auditoría
        categoria = "Otros"
        accion = f"{method} {path}"
        entidad = "Desconocida"

        if is_login:
            categoria = "Autenticación"
            accion = "Inicio de Sesión"
            entidad = "Sesión"
        elif is_register:
            categoria = "Autenticación"
            accion = "Registro"
            entidad = "Registro"
        elif is_user_mgmt:
            categoria = "Gestión de Usuarios"
            entidad = "Usuario"
            if method == "POST":
                accion = "Creación de Usuario"
            elif method == "PUT":
                accion = "Actualización de Usuario"
            elif method == "DELETE":
                accion = "Eliminación de Usuario"
            elif method == "GET":
                accion = "Consulta de Usuarios"

        # Clasificar el resultado
        status_code = response.status_code
        if status_code < 400:
            resultado = f"Éxito ({status_code})"
        else:
            if status_code == 401:
                resultado = "No Autorizado (401)"
            elif status_code == 403:
                resultado = "Acceso Denegado (403)"
            else:
                resultado = f"Fallo ({status_code})"

        # 6. Estructurar el JSON de detalles
        event_data = {
            "actor": user_email,
            "origen_evento": "AWS_Usuarios",
            "metodo": method,
            "ruta": path,
            "tiempo_ms": round(process_time, 2),
            "categoria": categoria,
            "accion": accion,
            "resultado": resultado,
            "entidad": entidad
        }

        # 7. Guardar en base de datos PostgreSQL de forma segura
        db = SessionLocal()
        try:
            db_audit = Auditoria(
                usuario=user_email,
                categoria=categoria,
                accion=accion,
                resultado=resultado,
                entidad=entidad,
                detalles=json.dumps(event_data)
            )
            db.add(db_audit)
            db.commit()
        except Exception as db_err:
            print(f"Error guardando auditoría en base de datos: {db_err}")
        finally:
            db.close()

        # 8. Enviar mensaje a Kafka al tópico 'auditoria'
        if producer:
            try:
                producer.produce(
                    'auditoria',
                    value=json.dumps(event_data).encode('utf-8'),
                    callback=delivery_report
                )
                producer.poll(0)
            except Exception as kafka_err:
                print(f"Error enviando a Kafka: {kafka_err}")

        return response
