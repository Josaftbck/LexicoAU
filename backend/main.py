from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, register_facial, rostro, login_qr, logout
from dotenv import load_dotenv
import os

# ============================================================
# 🌎 Cargar variables de entorno (.env.local o .env.prod)
# ============================================================
env_file = ".env.prod" if os.getenv("PRODUCTION") == "1" else ".env.local"
if not os.path.exists(env_file):
    env_file = ".env"  # Fallback por si el archivo no existe
load_dotenv(env_file)
print(f"📂 Archivo de entorno cargado: {env_file}")

# ============================================================
# ⚙️ Inicializar la aplicación FastAPI
# ============================================================
app = FastAPI(
    title="simpAUT API",
    version="1.0.0",
    description="Backend REST API for simpAUT - Automata Recognition System"
)

# ============================================================
# 🔹 Configurar CORS (para conexión con React y producción)
# ============================================================
origins = [
    "http://localhost:5173",          # Frontend local
    "http://127.0.0.1:5173",          # Alternativo
    "https://lexion.daossystem.pro",  # Producción (DaosSystem)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 🔹 Incluir routers del sistema
# ============================================================
app.include_router(auth.router)
app.include_router(register_facial.router)
app.include_router(rostro.router)
app.include_router(login_qr.router)
app.include_router(logout.router)

# ============================================================
# 🧠 Ruta de prueba (verifica si la API está activa)
# ============================================================
@app.get("/")
def read_root():
    return {
        "ok": True,
        "mensaje": "✅ API simpAUT corriendo correctamente",
        "version": "1.0.0"
    }