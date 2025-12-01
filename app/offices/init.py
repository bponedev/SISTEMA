from flask import Blueprint


offices_bp = Blueprint('offices', __name__)


from . import routes # noqa: F401
