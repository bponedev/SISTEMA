from flask import Flask
from .db import init_db
import os

# Blueprints
from .auth.routes import auth_bp
from .users.routes import users_bp
from .offices.routes import offices_bp
from .records.routes import records_bp
from .pdf.routes import pdf_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "CHAVE-MUITO-SECRETA"
    app.config["DB_PATH"] = os.path.join(os.getcwd(), "database.db")

    # Inicializa banco de dados
    with app.app_context():
        init_db()

    # Registra todos os blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(offices_bp)
    app.register_blueprint(records_bp)
    app.register_blueprint(pdf_bp)

    return app
