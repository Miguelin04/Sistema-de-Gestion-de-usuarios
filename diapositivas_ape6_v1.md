# Presentación: Guía de Actividades Práctico-Experimental Nro. 6 (Versión 1 - AWS)

A continuación se presenta la estructura sugerida para las diapositivas de la defensa o exposición de la APE 6, enfocada **únicamente en la primera versión** del proyecto desplegado en AWS.

---

## Diapositiva 1: Portada
**Título:** Análisis y creación de una Organización en DevOps. 
**Subtítulo:** DevOps para proyecto TFA - Versión 1 (AWS)
**Asignatura:** Computación en la Nube - Ciclo 6 "A"
**Integrantes:** 
- Stiven Jimenez
- David Guamán
- Miguel Luna
**Docente:** Ing. Roberth Figueroa Díaz

---

## Diapositiva 2: Objetivos de la Práctica
*(Puntos clave con viñetas para no saturar la diapositiva)*
- Comprender los principios y objetivos fundamentales del enfoque **DevOps**.
- Diseñar e implementar pipelines para la **automatización** del flujo de desarrollo.
- Aplicar prácticas de **Integración Continua (CI)** mediante repositorios colaborativos (GitHub).
- Desplegar una primera versión funcional del módulo de gestión de usuarios en la nube (**AWS**).

---

## Diapositiva 3: Arquitectura y Metodología (Versión 1)
**Enfoque de Desarrollo:**
- **Control de Versiones:** Uso de GitHub para gestionar el código fuente (`release/v1-aws`).
- **Orquestación:** Empaquetado monolítico utilizando **Docker y Docker Compose**.
- **Infraestructura:** Despliegue en la nube pública de Amazon Web Services (AWS).
- **Módulo Limitado:** Se aisló y desplegó exclusivamente el módulo base de Gestión de Usuarios.

---

## Diapositiva 4: Paso 1 - Aprovisionamiento en AWS
**Creación de la Instancia EC2:**
- **Máquina Virtual:** Tipo `t3.micro` con Ubuntu Server 22.04 LTS.
- **Configuración de Red (Security Group):**
  - **Puerto 22 (SSH):** Para administración remota de la instancia.
  - **Puerto 80 (HTTP):** Para exponer la interfaz web (Frontend).
  - **Puerto 8000 (API):** Para comunicación del Backend (FastAPI).

*(Nota para la exposición: Aquí se debe mostrar la "Captura 1" del panel de AWS con la instancia "Running")*

---

## Diapositiva 5: Paso 2 - Despliegue del Sistema
**Uso de Docker Compose en AWS:**
La arquitectura empaquetada se compone de 3 servicios principales corriendo en la misma instancia EC2:
1. **Frontend:** Interfaz de usuario (React/Vite) expuesta en el puerto 80.
2. **Backend:** API REST (FastAPI) en el puerto 8000.
3. **Base de Datos:** PostgreSQL para persistencia de datos.

*(Nota para la exposición: Aquí se debe incluir la "Captura 2" del comando `docker ps` mostrando los contenedores activos)*

---

## Diapositiva 6: Resultados y Validación
**Validación del Entorno DevOps (V1):**
- **Servicio:** Módulo de Autenticación en AWS.
- **Endpoint Web:** `http://3.21.50.248.nip.io/`
- **Comportamiento Observado:** Creación exitosa de usuarios y retorno de Token JWT tras ingresar credenciales válidas.
- **Estado:** ✅ Verificado.

*(Nota para la exposición: Mostrar la "Captura 3" del Login/Registro funcionando en la IP pública)*

---

## Diapositiva 7: Principios y Objetivos DevOps
*(Basado en las Preguntas de Control)*
- **¿Qué es DevOps?** Metodología que unifica desarrollo y operaciones fomentando la colaboración y automatización.
- **Principios Clave:**
  - Integración y Entrega Continua (CI/CD).
  - Adopción de Microservicios y Contenedores (Docker).
  - Ciclos de retroalimentación en tiempo real.
- **Objetivos:** Acelerar la entrega de software, maximizar la calidad y optimizar la infraestructura de TI.

---

## Diapositiva 8: Etapas del Ciclo de Vida DevOps
*(Diagrama visual sugerido de un infinito con las 8 etapas)*
1. **Planificación:** Definición del sistema.
2. **Codificación:** Control de versiones (Git).
3. **Construcción (Build):** Imágenes de contenedores.
4. **Pruebas (Test):** Integración continua (CI).
5. **Lanzamiento (Release):** Etiquetado inmutable de versiones.
6. **Despliegue (Deploy):** Entrega automatizada (CD).
7. **Operación:** Gestión dinámica de recursos.
8. **Monitorización:** Logs y métricas en tiempo real.

---

## Diapositiva 9: SDLC Tradicional vs SDLC en la Nube
*(Tabla comparativa resumida)*

| Característica | Tradicional | En la Nube (DevOps) |
| :--- | :--- | :--- |
| **Enfoque** | Cambios manuales (scripts paso a paso) | Declarativo (YAML, Docker-compose) |
| **Infraestructura** | Servidores propios, capacidad fija | Pago por uso, escalable (AWS) |
| **Despliegue** | Manual y escalabilidad vertical | Automatizado (CI/CD) y horizontal |
| **Arquitectura** | Monolítica rígida | Contenedores portátiles |

---

## Diapositiva 10: Conclusiones (Versión 1)
- La adopción de contenedores (Docker) facilitó la portabilidad del entorno de desarrollo a producción en AWS sin problemas de compatibilidad.
- El uso de EC2 demostró ser eficaz para un prototipo rápido (monolítico), preparando el terreno para la siguiente fase de microservicios y escalado horizontal.
