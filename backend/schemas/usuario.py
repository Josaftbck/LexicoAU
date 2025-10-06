from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    usuario: str
    email: EmailStr
    nombre_completo: str
    password: str
    telefono: str

class UsuarioLogin(BaseModel):
    usuario: str
    password: str