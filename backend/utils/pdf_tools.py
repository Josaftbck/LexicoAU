from reportlab.lib.pagesizes import landscape, A7
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black, white
import io
import base64
import os

def generar_credencial_pdf(nombre, correo, usuario, telefono, qr_base64, rostro_base64, output_path):
    """
    Genera una credencial PDF con plantilla, rostro, QR y datos del usuario.
    """
    # Tamaño y orientación
    pdf = canvas.Canvas(output_path, pagesize=landscape(A7))
    width, height = landscape(A7)

    # Fondo (usa plantilla si existe)
    plantilla_path = os.path.join("pruebas", "plantillas", "plantilla_credencial.png")
    if os.path.exists(plantilla_path):
        pdf.drawImage(plantilla_path, 0, 0, width=width, height=height)
    else:
        pdf.setFillColorRGB(1, 1, 1)
        pdf.rect(0, 0, width, height, fill=True)

    # Encabezado
    pdf.setFillColor(black)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(20, height - 25, "SISTEMA simpAUT")

    # Información del usuario
    pdf.setFont("Helvetica", 9)
    pdf.drawString(20, height - 45, f"Nombre: {nombre}")
    pdf.drawString(20, height - 60, f"Usuario: {usuario}")
    pdf.drawString(20, height - 75, f"Correo: {correo}")
    pdf.drawString(20, height - 90, f"Teléfono: {telefono}")

    # Imagen del rostro (segmentado)
    if rostro_base64:
        try:
            rostro_data = io.BytesIO(base64.b64decode(rostro_base64))
            pdf.drawImage(ImageReader(rostro_data), 20, 30, width=70, height=70, mask='auto')
        except Exception as e:
            print(f"⚠️ Error al agregar rostro: {e}")

    # Código QR
    try:
        qr_data = io.BytesIO(base64.b64decode(qr_base64))
        pdf.drawImage(ImageReader(qr_data), width - 100, 30, width=70, height=70, mask='auto')
    except Exception as e:
        print(f"⚠️ Error al agregar QR: {e}")

    # Firma inferior
    pdf.setFont("Helvetica-Oblique", 7)
    pdf.setFillColorRGB(0.2, 0.2, 0.2)
    pdf.drawRightString(width - 10, 10, "Credencial generada automáticamente — simpAUT")

    # Guardar PDF
    pdf.showPage()
    pdf.save()

    print(f"✅ Credencial PDF generada en: {output_path}")
    return output_path