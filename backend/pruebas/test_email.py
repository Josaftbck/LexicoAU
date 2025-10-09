import sys, os
# ✅ Agregar la carpeta /backend al path para reconocer 'utils'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.email_smtp import enviar_credencial_pdf

# Ruta del PDF de prueba (puedes cambiarla si ya generas una credencial)
pdf_path = "pruebas/credenciales/demo_credencial.pdf"

# Enviar correo de prueba
enviar_credencial_pdf(
    destinatario="wleona@miumg.edu.gt",  # 👈 pon aquí tu correo real
    nombre_usuario="Josafat Alvarado",
    pdf_path=pdf_path
)