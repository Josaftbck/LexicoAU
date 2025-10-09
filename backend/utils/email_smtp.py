# backend/utils/email_smtp.py
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
from pathlib import Path

# ============================================================
# 🧩 Cargar archivo .env (prioridad: .env.local → .env)
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent  # → /backend
env_path = BASE_DIR / ".env.local"
if not env_path.exists():
    env_path = BASE_DIR / ".env"

print(f"📂 Cargando configuración desde: {env_path}")
load_dotenv(dotenv_path=env_path)

# ============================================================
# 🔹 Variables de entorno (con valores por defecto seguros)
# ============================================================
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME)
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_USE_TLS = os.getenv("MAIL_STARTTLS", "True").lower() == "true"

# ============================================================
# ✉️ Envío de correo con PDF adjunto
# ============================================================
def enviar_credencial_pdf(destinatario: str, nombre_usuario: str, pdf_path: str):
    """
    Envía un correo electrónico con la credencial PDF adjunta usando Gmail SMTP.
    """
    try:
        if not MAIL_USERNAME or not MAIL_PASSWORD:
            raise ValueError("⚠️ MAIL_USERNAME o MAIL_PASSWORD no están definidos en .env")

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"El archivo PDF no existe: {pdf_path}")

        # Construir el mensaje
        msg = MIMEMultipart()
        msg["From"] = MAIL_FROM
        msg["To"] = destinatario
        msg["Subject"] = f"🎫 Credencial de acceso - simpAUT"

        cuerpo_html = f"""
        <div style="font-family: Arial, sans-serif; text-align:center;">
            <h2>👋 Hola {nombre_usuario}</h2>
            <p>Tu registro ha sido completado exitosamente.</p>
            <p>Adjunto encontrarás tu credencial en PDF con código QR para acceder al sistema.</p>
            <p style="font-size:12px; color:gray;">Si no solicitaste este correo, ignóralo.</p>
        </div>
        """
        msg.attach(MIMEText(cuerpo_html, "html"))

        # Adjuntar PDF
        with open(pdf_path, "rb") as f:
            pdf_part = MIMEApplication(f.read(), _subtype="pdf")
            pdf_part.add_header(
                "Content-Disposition",
                "attachment",
                filename=f"Credencial_{nombre_usuario}.pdf"
            )
            msg.attach(pdf_part)

        # Conectar al servidor SMTP
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            if MAIL_USE_TLS:
                server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Correo enviado exitosamente a {destinatario}")
        return True

    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")
        return False