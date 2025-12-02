from flask import (
    render_template, request, redirect, url_for, session, send_file
)
from datetime import datetime
from .db import get_conn
import pdfkit
from io import BytesIO
from app import create_app

app = create_app()

# -----------------------------------
# LOGIN
# -----------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND senha=?", (email, senha))
        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]
            return redirect("/dashboard")
        else:
            return render_template("login.html", erro=True)

    return render_template("login.html")


# -----------------------------------
# DASHBOARD
# -----------------------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html", usuario=session["user"])


# -----------------------------------
# USUÁRIOS
# -----------------------------------
@app.route("/usuarios")
def usuarios():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email FROM users")
    lista = cur.fetchall()
    conn.close()

    return render_template("usuarios.html", usuarios=lista)


# -----------------------------------
# REGISTROS – LISTAR
# -----------------------------------
@app.route("/registros")
def registros():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, descricao, data FROM registros")
    lista = cur.fetchall()
    conn.close()

    return render_template("registros.html", registros=lista)


# -----------------------------------
# REGISTROS – NOVO
# -----------------------------------
@app.route("/registros/novo", methods=["POST"])
def novo_registro():
    titulo = request.form["titulo"]
    descricao = request.form["descricao"]
    data = datetime.now().strftime("%d/%m/%Y")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO registros (titulo, descricao, data) VALUES (?, ?, ?)",
        (titulo, descricao, data),
    )
    conn.commit()
    conn.close()

    return redirect("/registros")


# -----------------------------------
# PDF
# -----------------------------------
@app.route("/pdf/<int:id>")
def gerar_pdf(id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM registros WHERE id=?", (id,))
    registro = cur.fetchone()
    conn.close()

    if not registro:
        return "Registro não encontrado"

    html = f"""
    <h1>{registro[1]}</h1>
    <p>{registro[2]}</p>
    <p>Data: {registro[3]}</p>
    """

    pdf = pdfkit.from_string(html, False)
    return send_file(BytesIO(pdf), as_attachment=True, download_name="registro.pdf")
