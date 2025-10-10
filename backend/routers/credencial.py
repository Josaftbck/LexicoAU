# backend/routers/credencial.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.email_smtp import enviar_credencial_pdf
import base64, tempfile, os

router = APIRouter(prefix="/credencial", tags=["Credencial"])

class CredencialData(BaseModel):
    email: str
    nombre_usuario: str
    pdf_base64: str

@router.post("/enviar")
async def enviar_credencial(data: CredencialData):
    # 1) Decodificar el PDF Base64
    try:
        pdf_bytes = base64.b64decode(data.pdf_base64)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF Base64 inválido: {e}")

    # 2) Guardar temporal para adjuntar al correo
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(pdf_bytes)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo crear archivo temporal: {e}")

    # 3) (Opcional) Guardar copia persistente
    try:
        os.makedirs("pruebas/credenciales", exist_ok=True)
        out_path = os.path.join("pruebas/credenciales", f"cred_{data.nombre_usuario}.pdf")
        with open(out_path, "wb") as f:
            f.write(pdf_bytes)
        print(f"✅ PDF guardado correctamente en {out_path}")
    except Exception as e:
        print(f"⚠️ No se pudo guardar copia persistente: {e}")
        out_path = None

    # 4) Enviar correo con el adjunto
    try:
        enviar_credencial_pdf(
            destinatario=data.email,
            nombre_usuario=data.nombre_usuario,
            pdf_path=tmp_path
        )
        print(f"📧 Credencial enviada a {data.email}")
    except Exception as e:
        # Limpieza y error
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        raise HTTPException(status_code=500, detail=f"Error al enviar correo: {e}")

    # 5) Limpieza del temporal y respuesta
    try:
        os.remove(tmp_path)
    except Exception:
        pass

    return {
        "ok": True,
        "mensaje": f"Credencial enviada a {data.email}",
        "guardado_local": out_path is not None
    }
