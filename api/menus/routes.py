from flask import Blueprint, session

from api import check_login
from api.menus.services import get_menus

menus_bp = Blueprint('menus', __name__, url_prefix="/api/v1/menus")


@menus_bp.route('/fetch', methods=['GET'])
@check_login
def fetch_menus():
    user: dict = session.get('user_info')
    return get_menus(user.get('id'))
