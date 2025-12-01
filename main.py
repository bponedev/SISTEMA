from flask import Flask
import os

# Importar blueprints
from app.auth.routes import auth_bp
from app.users.routes import users_bp
from app.offices.routes import offices_bp
from app.records.routes import records_bp
from app.pdf.routes import pdf_bp

from app.db import init_db

# Instância principal do Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "CHAVE-MUITO-SECRETA"
app.config["DB_PATH"] = os.path.join(os.getcwd(), "database.db")

# Inicializar o banco
with app.app_context():
    init_db()

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(offices_bp)
app.register_blueprint(records_bp)
app.register_blueprint(pdf_bp)
