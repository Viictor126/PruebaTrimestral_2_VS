from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from auth import router as auth_router
from deps import get_current_user

from db import get_db
from models import Incidencias

app = FastAPI(
    title="FastApi-incidencias",
    description="Api de incidencias con fastApi",
    version="1.0.0"
)

app.include_router(auth_router)

class IncidenciaCreate(BaseModel):
    titulo: str = Field(min_length=1)
    descripcion: str = Field(min_length=1)
    prioridad: str = Field(min_length=1)
    estado: str = Field(min_length=1)

class IncidenciaResponse(IncidenciaCreate):
    id: int
    class Config:
        from_attributes = True # pydantic v2

@app.get("/")
def root():
    return {"ok": True, "mensaje": "FastAPI funcionando Ve a http://127.0.0.1:8000/docs"}

@app.get("/privado")
def privado(usuario: str = Depends(get_current_user)):
    return {"mensaje": f"Hola {usuario}, estás autenticado"}

@app.get("/incidencias", response_model=list[IncidenciaResponse])
def todas_incidencias(db: Session = Depends (get_db)):
    return db.query(Incidencias).all()

@app.post("/incidencias", response_model=IncidenciaResponse, status_code=201)
def crear_incidencia(incidencia: IncidenciaCreate, db: Session = Depends(get_db), usuario: str = Depends(get_current_user)):
    nuevo = Incidencias(titulo=incidencia.titulo, descripcion=incidencia.descripcion, prioridad=incidencia.prioridad, estado=incidencia.estado)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo