from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []

templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    nombre: str
    apellido: str
    dni: str
    fecha_nacimiento: str
    direccion: str


@app.post("/users/", response_model=User)
async def create_user(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    dni: str = Form(...),
    fecha_nacimiento: str = Form(...),
    direccion: str = Form(...),
):
    for user in users:
        if user.nombre == nombre and user.apellido == apellido and user.dni == dni:
            raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        nombre=nombre, apellido=apellido, dni=dni, fecha_nacimiento=fecha_nacimiento, direccion=direccion
    )
    users.append(user)
    return templates.TemplateResponse("index.html", {"request": request, "users": users})


@app.get("/users/", response_model=List[User])
async def get_users(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "users": users})


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, request: Request):
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("index.html", {"request": request, "users": [users[user_id]]})


@app.get("/users/{user_id}/update/")
async def get_update_user(user_id: int, request: Request):
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("update.html", {"request": request, "user": users[user_id], "user_id": user_id})


@app.put("/users/{user_id}/update/", response_model=User)
async def update_user(
    user_id: int,
    updated_user: User,
    request: Request,
):
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")

    users[user_id] = updated_user
    return updated_user

@app.post("/users/{user_id}/delete/", response_model=User)
async def delete_user(user_id: int, request: Request):
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")

    deleted_user = users.pop(user_id)
    return templates.TemplateResponse("index.html", {"request": request, "users": users})
