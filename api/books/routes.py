from flask import Blueprint, request

from api import check_login
from api.books.services import fetch_all_books, classify_books, fetch_bk, insert_book, rec_bks

books_bp = Blueprint('books', __name__, url_prefix="/api/v1/books")


@books_bp.route('/', methods=['GET'])
@check_login
def fetch_books():
    return fetch_all_books()


@books_bp.route('/classification', methods=['GET'])
@check_login
def classification():
    return classify_books()


@books_bp.route('/view/<int:book_id>', methods=['GET'])
@check_login
def fetch_book(book_id):
    return fetch_bk(book_id)


@books_bp.route('/insert', methods=['POST'])
@check_login
def isrt_book():
    data = request.json
    return insert_book(data)


@books_bp.route('/recBks', methods=['GET'])
@check_login
def rec_books():
    return rec_bks()