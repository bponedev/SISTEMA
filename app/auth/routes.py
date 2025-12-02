from flask import Blueprint, render_template, request, redirect, url_for
# from app.db import get_conn
# from werkzeug.security import check_password_hash


auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="../templates")

# suas rotas continuam iguais



# ===============================================================
# LOGIN
# ===============================================================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT id, usuario, senha FROM usuarios WHERE usuario = ?", (usuario,))
        user = cur.fetchone()

        if user and check_password_hash(user[2], senha):
            session["usuario_id"] = user[0]
            session["usuario_nome"] = user[1]
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("users.dashboard"))
        else:
            flash("Usuário ou senha inválidos", "danger")

    return render_template("auth/login.html")


# ===============================================================
# LOGOUT
# ===============================================================
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da conta.", "info")
    return redirect(url_for("auth.login"))
