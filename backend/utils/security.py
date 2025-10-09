from passlib.context import CryptContext
import os
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

# ============================================================
# 🧩 CONFIGURACIÓN GENERAL
# ============================================================

# Configura bcrypt como algoritmo de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Máxima longitud segura para bcrypt
MAX_PASSWORD_LENGTH = 72

# Cargar variables del entorno
load_dotenv()

# Clave secreta para JWT
SECRET_KEY = os.getenv("JWT_SECRET", "clave-super-secreta")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # duración del token en minutos


# ============================================================
# 🔐 FUNCIONES DE CONTRASEÑAS
# ============================================================

def hash_password(password: str) -> str:
    """
    Hashea una contraseña si es válida (máximo 72 caracteres para bcrypt).
    """
    if len(password.encode("utf-8")) > MAX_PASSWORD_LENGTH:
        raise ValueError("❌ La contraseña no puede tener más de 72 caracteres")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que la contraseña plana coincida con el hash almacenado.
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================
# 🧠 FUNCIONES JWT (JSON Web Token)
# ============================================================

def crear_token_jwt(data: dict, expires_delta: int = None) -> str:
    """
    Crea un token JWT con expiración configurable (por defecto 15 minutos).
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verificar_token_jwt(token: str):
    """
    Decodifica y valida un token JWT.
    Retorna los datos si el token es válido; lanza excepción si no lo es.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("❌ El token ha expirado.")
    except jwt.InvalidTokenError:
        raise ValueError("❌ Token inválido.")