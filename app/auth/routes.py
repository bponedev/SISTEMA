from flask import render_template, request, redirect, url_for, session, flash
from . import auth_bp
from app.db import query
from functools import wraps

# Decorador de login
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrap

# Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        user = query(
            "SELECT * FROM users WHERE usuario=? AND senha=?",
            (usuario, senha),
            one=True
        )

        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect(url_for("records.home"))

        flash("Usuário ou senha inválidos", "danger")

    return render_template("login.html")

# Logout
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
