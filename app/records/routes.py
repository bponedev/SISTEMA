from flask import render_template, request, redirect, url_for, flash
from . import records_bp
from app.db import get_conn

records_bp = Blueprint("records", __name__, url_prefix="/records", template_folder="../templates")



@records_bp.route('/')
def index():
offices = []
conn = get_conn()
c = conn.cursor()
c.execute('SELECT office_key, display_name FROM offices ORDER BY display_name')
rows = c.fetchall()
conn.close()
offices = [{'key': r[0], 'display': r[1]} for r in rows]
return render_template('index.html', offices=offices)




@records_bp.route('/submit', methods=['POST'])
def submit():
nome = request.form.get('nome')
cpf = request.form.get('cpf')
escritorio = request.form.get('escritorio', 'CENTRAL')
tipo_acao = request.form.get('tipo_acao')
data_fechamento = request.form.get('data_fechamento')
pendencias = request.form.get('pendencias')
numero_processo = request.form.get('numero_processo')
data_protocolo = request.form.get('data_protocolo')
observacoes = request.form.get('observacoes')
captador = request.form.get('captador')


conn = get_conn()
c = conn.cursor()
c.execute('INSERT INTO registros (nome, cpf, escritorio_nome, tipo_acao, data_fechamento, pendencias, numero_processo, data_protocolo, observacoes, captador) VALUES (?,?,?,?,?,?,?,?,?,?)',
(nome, cpf, escritorio, tipo_acao, data_fechamento, pendencias, numero_processo, data_protocolo, observacoes, captador))
conn.commit()
conn.close()
flash('Registro salvo com sucesso.', 'success')
return redirect(url_for('records.index'))




@records_bp.route('/table')
def table():
office = request.args.get('office', 'CENTRAL')
conn = get_conn()
c = conn.cursor()
c.execute('SELECT * FROM registros WHERE escritorio = ? ORDER BY id DESC', (office,))
rows = c.fetchall()
conn.close()
return render_template('table.html', registros=rows)
