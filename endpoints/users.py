from models import Users
from flask import Blueprint

bp = Blueprint('user', __name__)


@bp.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = Users.query.filter_by(username=username).first()

    if user:
        return {'payload': user}, 200
    else:
        return {'error': "User not found"}, 404
