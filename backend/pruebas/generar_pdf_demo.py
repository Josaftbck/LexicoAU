from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

pdf_path = "pruebas/credenciales/demo_credencial.pdf"
c = canvas.Canvas(pdf_path, pagesize=A4)
c.setFont("Helvetica-Bold", 20)
c.drawString(100, 750, "Credencial de prueba simpAUT")
c.setFont("Helvetica", 14)
c.drawString(100, 720, "Nombre: Josafat Alvarado")
c.drawString(100, 700, "Email: josafat@example.com")
c.drawString(100, 680, "Código QR: (simulado)")
c.save()

print(f"✅ PDF generado en: {pdf_path}")