
# TEMA 1 - API REST
# Ejemplo 08: Organización mediante contactos y tareas
#
# Para ejecutar:
# .7.venv/bin/fastapi dev 09_contacts/main.py
#
# Documentación interactiva
# http://127.0.0.1.8000/docs

from fastapi import FastAPI
from contacts import contactos, tareas

# Creamos la aplicación principal.
app = FastAPI(title="Ejemplo 09 - Contactos y tarea")

# Incorporamos los contactos a nuestra aplicación.
app.include_router(
    contactos.router,
    prefix="/contactos",
    tags=["Contactos"]
)

app.include_router(
    tareas.router,
    prefix="/tareas",
    tags=["Tareas"]
)

# GET http://127.0.0.1:8000/
@app.get("/")
def inicio():
    return {"mensaje": "API REST de Contactos y Tareas"}