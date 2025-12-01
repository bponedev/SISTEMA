from flask import render_template, request, redirect, url_for, session
from . import users_bp
from app.db import query, execute
from app.auth.routes import login_required

def admin_required():
    return session.get("role") == "ADMIN"

# LISTAR USUÁRIOS
@users_bp.route("/")
@login_required
def list():
    if not admin_required():
        return "Acesso negado."

    users = query("SELECT * FROM users ORDER BY id DESC")
    return render_template("users/list.html", users=users)

# CRIAR USUÁRIO
@users_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if not admin_required():
        return "Acesso negado."

    if request.method == "POST":
        execute("""
        INSERT INTO users (usuario, senha, role)
        VALUES (?, ?, ?)
        """, (
            request.form["usuario"],
            request.form["senha"],
            request.form["role"]
        ))
        return redirect(url_for("users.list"))

    return render_template("users/create.html")

# EDITAR USUÁRIO
@users_bp.route("/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit(user_id):
    if not admin_required():
        return "Acesso negado."

    user = query("SELECT * FROM users WHERE id=?", (user_id,), one=True)

    if request.method == "POST":
        execute("""
        UPDATE users SET usuario=?, senha=?, role=?
        WHERE id=?
        """, (
            request.form["usuario"],
            request.form["senha"],
            request.form["role"],
            user_id
        ))
        return redirect(url_for("users.list"))

    return render_template("users/edit.html", user=user)
