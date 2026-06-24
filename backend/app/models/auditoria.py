# Autor: Antigravity
# Fecha: 24/06/2026
# Version: 1.0

from datetime import datetime
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base
from sqlalchemy.sql import func

class Auditoria(Base):
    __tablename__ = "auditoria"

    id_auditoria: Mapped[int] = mapped_column(primary_key=True, index=True)
    fecha: Mapped[datetime] = mapped_column(DateTime, default=func.now(), server_default=func.now(), nullable=False)
    usuario: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    categoria: Mapped[str] = mapped_column(String(100), nullable=False)
    accion: Mapped[str] = mapped_column(String(100), nullable=False)
    resultado: Mapped[str] = mapped_column(String(100), nullable=False)
    entidad: Mapped[str] = mapped_column(String(100), nullable=False)
    detalles: Mapped[str] = mapped_column(Text, nullable=True)
