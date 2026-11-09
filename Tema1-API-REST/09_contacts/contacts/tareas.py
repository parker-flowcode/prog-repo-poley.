
# TEMA 1 - API REST
# Ejemplo 09: Contactos de tareas
#
# Este archivo no se ejecuta directamente
# Lo incorpora main.py mediante include_contacto().

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date

router = APIRouter()

# Modelo de tarea+
class TareaCreate(BaseModel):
    name: str
    fecha_inicio: date
    fecha_fin: date

class Tarea(TareaCreate):
    id: int

# Lista de tareas.
tareas_list = [
    Tarea(id=1, name="Entrevistar al cliente", fecha_inicio=date(2026, 5, 1), fecha_fin=date(2026,5,30)),
    Tarea(id=2, name="Diseñar UI", fecha_inicio=date(2026,8,5), fecha_fin=date(2026,8,25)),
    Tarea(id=3, name="Programar en Python",fecha_inicio=date(2026,9,1), fecha_fin=date(2026,9,30)),
    Tarea(id=4, name="Configurar Firebase", fecha_inicio=date(2026,10,8), fecha_fin=date(2026,10,20))
]


# GET http://127.0.0.1.8000/tareas
# Devuelve todas las tareas
@router.get("")
def obtener_tareas():
    return tareas_list


# GET http://127.0.0.1.8000/tareas/2
# Devuelve un producto por su ID.
@router.get("/{id}")
def obtener_producto(id: int):

    for producto in tareas_list:
        if producto.id == id:
            return producto

    raise HTTPException(
        status_code=404,
        detail="Tarea no encontrada"
    )