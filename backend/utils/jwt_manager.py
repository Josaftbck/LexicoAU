from jose import JWTError, jwt
from datetime import datetime, timedelta

# Configuración del token
SECRET_KEY = "simpAUT_ClaveUltraSecreta2025"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🔐 Crear token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Verificar token y retornar payload
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # contiene los datos codificados, por ejemplo: {"sub": "jose123"}
    except JWTError:
        return None
    

    