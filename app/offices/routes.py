from flask import render_template, request, redirect, url_for
from . import offices_bp
from app.db import query, execute
from app.auth.routes import login_required

# LISTAR
@offices_bp.route("/")
@login_required
def list():
    offices = query("SELECT * FROM offices ORDER BY nome ASC")
    return render_template("offices/list.html", offices=offices)

# CRIAR
@offices_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        execute("INSERT INTO offices (nome) VALUES (?)",
                (request.form["nome"],))
        return redirect(url_for("offices.list"))
    return render_template("offices/create.html")

# EDITAR
@offices_bp.route("/edit/<int:office_id>", methods=["GET", "POST"])
@login_required
def edit(office_id):
    office = query("SELECT * FROM offices WHERE id=?", (office_id,), one=True)

    if request.method == "POST":
        execute("UPDATE offices SET nome=? WHERE id=?",
                (request.form["nome"], office_id))
        return redirect(url_for("offices.list"))

    return render_template("offices/edit.html", office=office)
