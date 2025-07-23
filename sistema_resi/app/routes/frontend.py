from flask import Blueprint

bp = Blueprint('frontend', __name__)


@bp.route('/')
def index():
    return 'Area dipendenti'
