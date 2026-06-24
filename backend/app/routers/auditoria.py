# Autor: Antigravity
# Fecha: 24/06/2026
# Version: 1.0

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from app.database.session import get_db
from app.core.deps import get_current_admin
from app.models.auditoria import Auditoria
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/auditoria",
    tags=["Auditoría de Eventos (Admin)"]
)

class AuditoriaResponse(BaseModel):
    id_auditoria: int
    fecha: datetime
    usuario: str
    categoria: str
    accion: str
    resultado: str
    entidad: str
    detalles: Optional[str]

    class Config:
        from_attributes = True

@router.get("/", response_model=List[AuditoriaResponse])
def listar_auditorias(
    skip: int = 0,
    limit: int = 100,
    usuario: Optional[str] = None,
    categoria: Optional[str] = None,
    entidad: Optional[str] = None,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin)
) -> Any:
    """
    Obtiene la lista de todos los registros de auditoría.
    Ruta protegida: Solo accesible por Administradores.
    """
    query = db.query(Auditoria)
    
    if usuario:
        query = query.filter(Auditoria.usuario.ilike(f"%{usuario}%"))
    if categoria:
        query = query.filter(Auditoria.categoria == categoria)
    if entidad:
        query = query.filter(Auditoria.entidad == entidad)
        
    auditorias = query.order_by(Auditoria.fecha.desc()).offset(skip).limit(limit).all()
    return auditorias
