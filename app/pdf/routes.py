from flask import send_file
from reportlab.pdfgen import canvas
import io
from . import pdf_bp
from app.db import query
from app.auth.routes import login_required

@pdf_bp.route("/pdf")
@login_required
def export_pdf():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    registros = query("SELECT * FROM registros ORDER BY id DESC")

    y = 800
    p.setFont("Helvetica", 12)
    p.drawString(50, y, "Relatório de Registros")
    y -= 30

    for r in registros:
        texto = f"{r['id']} - {r['nome']} - {r['cpf']} - {r['escritorio']}"
        p.drawString(50, y, texto)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.save()
    buffer.seek(0)

    return send_file(buffer,
                     as_attachment=True,
                     download_name="registros.pdf")
