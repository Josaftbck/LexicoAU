from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth  # 👈 Aquí importas el router de autenticación
from routers import register_facial 

app = FastAPI(
    title="simpAUT API",
    version="1.0.0",
    description="Backend REST API for simpAUT - Automata Recognition System"
)

# Configura CORS
origins = [
    "http://localhost:5173",  # frontend local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar router de autenticación
app.include_router(auth.router)
app.include_router(register_facial.router)

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "API simpAUT corriendo correctamente"}