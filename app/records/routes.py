from flask import render_template, request, redirect, url_for
from . import records_bp
from app.db import query, execute
from app.auth.routes import login_required

# HOME
@records_bp.route("/")
@login_required
def home():
    offices = query("SELECT nome FROM offices ORDER BY nome ASC")
    return render_template("records/create.html", offices=offices)

# SALVAR REGISTRO
@records_bp.route("/submit", methods=["POST"])
@login_required
def submit():
    execute("""
    INSERT INTO registros (
        nome, cpf, escritorio, tipo_acao, data_fechamento,
        pendencias, numero_processo, data_protocolo,
        observacoes, captador
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        request.form["nome"],
        request.form["cpf"],
        request.form["escritorio"],
        request.form["tipo_acao"],
        request.form["data_fechamento"],
        request.form["pendencias"],
        request.form["numero_processo"],
        request.form["data_protocolo"],
        request.form["observacoes"],
        request.form["captador"],
    ))

    return redirect(url_for("records.list"))

# LISTAR
@records_bp.route("/registros")
@login_required
def list():
    r = query("SELECT * FROM registros ORDER BY id DESC")
    return render_template("records/list.html", registros=r)
