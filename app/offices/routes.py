from flask import render_template, request, redirect, url_for, flash
from . import offices_bp
from app.db import get_conn

offices_bp = Blueprint("offices", __name__, url_prefix="/offices", template_folder="../templates")



@offices_bp.route('/offices')
def offices_list():
conn = get_conn()
c = conn.cursor()
c.execute('SELECT office_key, display_name FROM offices ORDER BY display_name')
rows = c.fetchall()
conn.close()
offices = [{'key': r[0], 'display': r[1]} for r in rows]
return render_template('offices.html', offices=offices)




@offices_bp.route('/offices/create', methods=['POST'])
def offices_create():
name = request.form.get('office_name')
if not name:
flash('Nome inválido.', 'error')
return redirect(url_for('offices.offices_list'))
key = name.strip().upper().replace(' ', '_')
conn = get_conn()
c = conn.cursor()
c.execute('INSERT OR IGNORE INTO offices (office_key, display_name) VALUES (?, ?)', (key, name.upper()))
conn.commit()
conn.close()
flash('Escritório criado.', 'success')
return redirect(url_for('offices.offices_list'))
