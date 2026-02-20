from sqlalchemy import Column, Integer, String, Numeric
from db import Base

class Incidencias(Base):
    __tablename__ = "incidencias"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    prioridad = Column(String, nullable=False)
    estado = Column(String, nullable=False)