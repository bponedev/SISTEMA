from flask import send_file
from . import pdf_bp
from reportlab.pdfgen import canvas
import io
from app.db import get_conn




@pdf_bp.route('/export/pdf')
def export_pdf():
conn = get_conn()
c = conn.cursor()
c.execute('SELECT * FROM registros')
rows = c.fetchall()
conn.close()


buffer = io.BytesIO()
p = canvas.Canvas(buffer)
y = 800
p.setFont('Helvetica', 12)
p.drawString(50, y, 'Relatório de Registros')
y -= 30
for r in rows:
texto = f"{r[0]} - {r[1]} - {r[2]} - {r[3]}"
p.drawString(50, y, texto)
y -= 20
if y < 50:
p.showPage()
y = 800
p.save()
buffer.seek(0)
return send_file(buffer, as_attachment=True, download_name='registros.pdf', mimetype='application/pdf')
