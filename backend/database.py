import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# ==============================================
# 🔹 Cargar variables de entorno automáticamente
# ==============================================
env_file = ".env.prod" if os.getenv("PRODUCTION") == "true" else ".env.local"
load_dotenv(env_file)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ No se encontró DATABASE_URL en el archivo .env")

# ==============================================
# ⚙️ Configuración de la conexión
# ==============================================
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==============================================
# 📦 Dependencia para obtener sesión de DB
# ==============================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
