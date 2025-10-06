
from passlib.context import CryptContext

# Configura bcrypt como algoritmo de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Máxima longitud segura para bcrypt
MAX_PASSWORD_LENGTH = 72

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