from flask import Flask
from .db import init_db

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "CHAVE-SUPER-SECRETA"
    app.config["DB_PATH"] = "database.db"

    # inicia DB
    init_db()

    # importa rotas (isso registra tudo)
    from . import routes

    return app
