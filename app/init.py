from flask import Flask
from .db import init_db
import os

def register_blueprints(app):
    """Carrega blueprints individualmente sem quebrar o sistema."""
    from importlib import import_module

    modules = [
        ("app.auth.routes", "auth_bp"),
        ("app.users.routes", "users_bp"),
        ("app.offices.routes", "offices_bp"),
        ("app.records.routes", "records_bp"),
        ("app.pdf.routes", "pdf_bp"),
    ]

    for module_path, bp_name in modules:
        try:
            module = import_module(module_path)
            blueprint = getattr(module, bp_name)
            app.register_blueprint(blueprint)
            print(f"[OK] Blueprint carregado: {bp_name}")
        except Exception as e:
            print(f"[ERRO] Falha ao carregar {bp_name}: {e}")

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    app.config["SECRET_KEY"] = "CHAVE-MUITO-SECRETA"
    app.config["DB_PATH"] = os.path.join(os.getcwd(), "database.db")

    # Inicializa o banco
    with app.app_context():
        init_db()

    # Registra blueprints com tratamento de erro
    register_blueprints(app)

    return app
