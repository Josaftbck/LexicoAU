from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, register_facial, rostro, login_qr, logout, credencial
from dotenv import load_dotenv
import os
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.datastructures import UploadFile

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
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",      # 👈 nuevo puerto local
    "http://127.0.0.1:5174",      # 👈 alternativo
    "https://lexion.daossystem.pro",  # 👈 dominio producción
    "https://lexion-daossystem-pro.up.railway.app",  # 👈 dominio Railway si ya lo tienes
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 🧩 Middleware para permitir archivos grandes (hasta 50 MB)
# ============================================================
@app.middleware("http")
async def limit_request_body(request: Request, call_next):
    body = await request.body()
    if len(body) > 50 * 1024 * 1024:  # 50 MB
        return Response("❌ Archivo demasiado grande (>50 MB)", status_code=413)
    request._body = body
    return await call_next(request)

# ============================================================
# 🔹 Incluir routers del sistema
# ============================================================
app.include_router(auth.router)
app.include_router(register_facial.router)
app.include_router(rostro.router)
app.include_router(login_qr.router)
app.include_router(logout.router)
app.include_router(credencial.router)

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