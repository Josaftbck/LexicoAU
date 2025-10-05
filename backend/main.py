from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa tus routers (cuando los crees)
# from routers import users, recognition, etc

app = FastAPI(
    title="simpAUT API",
    version="1.0.0",
    description="Backend REST API for simpAUT - Automata Recognition System"
)

# Configura CORS
origins = [
    "http://localhost:5173",  # frontend local
    # "https://tudominio.com"  # si lo subes a producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Punto de prueba básico
@app.get("/")
def read_root():
    return {"message": "API simpAUT corriendo correctamente"}

# Incluye routers aquí cuando existan
# app.include_router(users.router)
# app.include_router(recognition.router)