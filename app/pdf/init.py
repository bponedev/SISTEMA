from flask import Blueprint

pdf_bp = Blueprint("pdf", __name__, url_prefix="/export")
