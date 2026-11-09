from datetime import date
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

# -------------------------------------------
# MODELOS DE DATOS
# -------------------------------------------

class ContactoCreate(BaseModel):
    nombre: str
    apellidos: str
    fecha_cumple: date

class Contacto(ContactoCreate):
    id: int

class ContactoPatch(BaseModel):
    nombre: str | None = None
    apellidos: str | None = None
    fecha_cumple: date | None = None

# -------------------------------------------
# LISTA QUE SIMULA UNA BASE DE DATOS
# -------------------------------------------

contactos_list = [
    Contacto(id=1, nombre="Paco", apellidos="Pérez", fecha_cumple=date(1990, 5, 15)),
    Contacto(id=2, nombre="María", apellidos="Martínez", fecha_cumple=date(1995, 8, 22)),
    Contacto(id=3, nombre="Lucía", apellidos="Rodríguez", fecha_cumple=date(1988, 12, 10))
]

# -------------------------------------------
# FUNCIÓN AUXILIAR
# -------------------------------------------

def buscar_contacto(id: int):
    for contacto in contactos_list:
        if contacto.id == id:
            return contacto
    raise HTTPException(status_code=404, detail="Contacto no encontrado")

# -------------------------------------------
# OPERACIONES
# -------------------------------------------

# GET http://127.0.0.1.8000/contactos
# Devuelve todas las tareas
@router.get("")
def obtener_contactos():
    return contactos_list

#GET http://127.0.0.1.8000/contactos/2
# Devuelve un contacto por su ID
@router.get("/{id}")
def obtener_contacto(id: int):
    return buscar_contacto(id)

#POST http://127.0.0.1.8000/contactos
# Añadimos un nuevo contacto
@router.post("", status_code=201, response_model=Contacto)
def crear_contacto(contacto: ContactoCreate):
    siguiente_id = max((c.id for c in contactos_list), default=0) + 1
    nuevo_contacto = Contacto(id=siguiente_id, **contacto.model_dump())
    contactos_list.append(nuevo_contacto)
    return nuevo_contacto

#PUT http://127.0.0.1.8000/contactos/2
# Modificamos un contacto por su ID

@router.put("/{id}", response_model=Contacto)
def modificar_contacto(id: int, datos: ContactoCreate):
    for posicion, contacto in enumerate(contactos_list):
        if contacto.id == id:
            contacto_modificado = Contacto(id=id, **datos.model_dump())
            contactos_list[posicion] = contacto_modificado
            return contacto_modificado
    raise HTTPException(status_code=404, detail="Contacto no encontrado")

@router.patch("/{id}", response_model=Contacto)
def modificar_contacto_parcial(id: int, datos: ContactoPatch):
    for posicion, contacto in enumerate(contactos_list):
        if contacto.id == id:
            cambios = datos.model_dump(exclude_unset=True, exclude_none=True)
            datos_actualizados = contacto.model_dump()
            datos_actualizados.update(cambios)
            contacto_modificado = Contacto(**datos_actualizados)
            contactos_list[posicion] = contacto_modificado
            return contacto_modificado
    raise HTTPException(status_code=404, detail="Contacto no encontrado")

@router.delete("/{id}")
def eliminar_contacto(id: int):
    for contacto in contactos_list:
        if contacto.id == id:
            contactos_list.remove(contacto)
            return {}
    raise HTTPException(status_code=404, detail="Contacto no encontrado")