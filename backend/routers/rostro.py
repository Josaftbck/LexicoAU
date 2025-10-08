from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.autenticacion_facial import AutenticacionFacial
from models.usuario import Usuario
import base64, requests

router = APIRouter(prefix="/rostro", tags=["Rostro"])

# ============================================================
# 🌐 SERVIDOR DE RECONOCIMIENTO FACIAL EXTERNO
# ============================================================
SERVER_URL = "http://www.server.daossystem.pro:3405/Rostro"

# ============================================================
# 🔹 FUNCIONES AUXILIARES
# ============================================================
def comparar_rostros(rostroA: str, rostroB: str):
    """
    Llama al endpoint externo para verificar similitud entre rostros.
    Retorna un JSON con campos: { resultado, score, status, ... }
    """
    payload = {"RostroA": rostroA, "RostroB": rostroB}
    response = requests.post(f"{SERVER_URL}/Verificar", json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al verificar rostro externo.")

    try:
        return response.json()
    except Exception:
        raise HTTPException(status_code=500, detail="Respuesta no válida del servidor externo.")


# ============================================================
# 🧠 LOGIN POR ROSTRO
# ============================================================
@router.post("/login")
async def login_por_rostro(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    📸 Recibe una imagen facial (archivo) y la compara contra los rostros
    registrados en la base de datos para identificar al usuario.
    """

    try:
        # 📷 1️⃣ Leer y convertir la imagen subida a Base64
        image_bytes = await file.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        # 🔍 2️⃣ Buscar todos los registros de autenticación facial
        registros = db.query(AutenticacionFacial).all()
        if not registros:
            raise HTTPException(status_code=404, detail="No hay rostros registrados en la base de datos")

        mejor_score = 0.0
        usuario_encontrado = None

        # 🧠 3️⃣ Comparar con cada rostro guardado
        for reg in registros:
            resultado = comparar_rostros(image_b64, reg.imagen_referencia)

            # Intentar convertir el score a número (puede venir como string)
            try:
                score = float(resultado.get("score", 0))
            except (ValueError, TypeError):
                score = 0.0

            # Si el resultado es válido y mejora el mejor score anterior
            if resultado.get("resultado") and score > mejor_score:
                mejor_score = score
                usuario_encontrado = db.query(Usuario).filter(Usuario.id == reg.usuario_id).first()

        # 🚫 4️⃣ Ninguna coincidencia aceptable
        if not usuario_encontrado or mejor_score < 0.85:
            return {
                "coincide": False,
                "score": mejor_score,
                "mensaje": "❌ No se encontró coincidencia facial válida"
            }

        # ✅ 5️⃣ Coincidencia encontrada
        return {
            "coincide": True,
            "usuario_id": usuario_encontrado.id,
            "nombre": usuario_encontrado.nombre_completo,
            "score": mejor_score,
            "mensaje": f"✅ Rostro coincide con {usuario_encontrado.nombre_completo}"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
