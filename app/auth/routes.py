from flask import render_template, request, redirect, url_for, flash, session
from . import auth_bp
from app.db import get_conn




@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
if request.method == 'POST':
username = request.form.get('usuario') or request.form.get('username')
password = request.form.get('senha') or request.form.get('password')
conn = get_conn()
c = conn.cursor()
c.execute('SELECT id, senha, role, active FROM users WHERE usuario = ?', (username,))
row = c.fetchone()
conn.close()
if not row:
flash('Usuário inválido.', 'error')
return render_template('login.html')
# NOTE: in V1 passwords are hashed — adapt if you store plaintext
stored = row[1]
if stored == password:
session['user_id'] = row[0]
session['role'] = row[2]
flash('Login efetuado.', 'success')
return redirect(url_for('index'))
flash('Usuário ou senha incorretos.', 'error')
return render_template('login.html')




@auth_bp.route('/logout')
def logout():
session.pop('user_id', None)
flash('Desconectado.', 'info')
return redirect(url_for('login'))
