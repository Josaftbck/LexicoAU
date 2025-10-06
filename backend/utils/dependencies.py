from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from utils.jwt_manager import SECRET_KEY, ALGORITHM
from database import SessionLocal
from models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    # Buscar el usuario en la base de datos
    db = SessionLocal()
    user = db.query(Usuario).filter(Usuario.usuario == username).first()
    db.close()
    if user is None or not user.activo:
        raise HTTPException(status_code=401, detail="Usuario no válido")
    
    return user