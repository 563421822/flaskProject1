from flask import Blueprint

from api import check_login
from api.lending.services import ftch_lend, delete_lending, lend_bk

lending_bp = Blueprint('lending', __name__, url_prefix="/api/v1/lending")


@lending_bp.route('/', methods=['GET'])
@check_login
def fetch_lending():
    return ftch_lend()


@lending_bp.route('/del/<int:lending_id>', methods=['GET'])
@check_login
def del_lending(lending_id):
    return delete_lending(lending_id)


@lending_bp.route('/lend/<int:book_id>', methods=['GET'])
@check_login
def lend_book(book_id):
    return lend_bk(book_id)
