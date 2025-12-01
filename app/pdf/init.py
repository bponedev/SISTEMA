from flask import Blueprint


pdf_bp = Blueprint('pdf', __name__)


from . import routes # noqa: F401
