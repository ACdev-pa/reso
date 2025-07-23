from flask import Blueprint

bp = Blueprint('backend', __name__, url_prefix='/admin')


@bp.route('/')
def index():
    return 'Area admin'
