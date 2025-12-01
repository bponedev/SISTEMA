from flask import render_template, request, redirect, url_for, flash
from . import users_bp
from app.db import get_conn




@users_bp.route('/admin/users')
def admin_users():
conn = get_conn()
c = conn.cursor()
c.execute('SELECT id, username, full_name, role, active, created_at FROM users ORDER BY id DESC')
rows = c.fetchall()
conn.close()
users = []
for r in rows:
users.append({'id': r[0], 'username': r[1], 'full_name': r[2], 'role': r[3], 'active': r[4]})
return render_template('admin_users.html', users=users)




@users_bp.route('/admin/users/create', methods=['GET', 'POST'])
def admin_users_create():
if request.method == 'POST':
username = request.form.get('username')
full_name = request.form.get('full_name')
password = request.form.get('password')
role = request.form.get('role', 'OPERADOR')
conn = get_conn()
c = conn.cursor()
try:
c.execute('INSERT INTO users (username, full_name, password_hash, role, active, created_at) VALUES (?,?,?,?,?,?)',
(username, full_name, password, role, 1, None))
conn.commit()
flash('Usuário criado.', 'success')
return redirect(url_for('users.admin_users'))
except Exception as e:
conn.rollback()
flash('Erro: ' + str(e), 'error')
finally:
conn.close()
return render_template('admin_users_create.html')
