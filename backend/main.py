from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, register_facial, rostro  # 👈 agregamos rostro

app = FastAPI(
    title="simpAUT API",
    version="1.0.0",
    description="Backend REST API for simpAUT - Automata Recognition System"
)

# ============================================================
# 🔹 Configurar CORS (para conexión con React)
# ============================================================
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 🔹 Incluir routers
# ============================================================
app.include_router(auth.router)
app.include_router(register_facial.router)
app.include_router(rostro.router)  # 👈 ahora sí se activa /rostro/login

# ============================================================
# 🔹 Ruta de prueba
# ============================================================
@app.get("/")
def read_root():
    return {"message": "API simpAUT corriendo correctamente ✅"}