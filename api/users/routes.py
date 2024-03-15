from flask import request, Blueprint, render_template, session, redirect, url_for

from api import check_login
from api.users.services import authenticate, qry_al_users, update_user, del_usr, add_usr

users_bp = Blueprint('users', __name__, url_prefix="/api/v1/users")


@users_bp.route('/login', methods=['GET'])
def login_user():
    if session.get('user_info'):
        return redirect(url_for('users.index'))
    return render_template('sign-in/login.html')


@users_bp.route('/doLogin', methods=['POST'])
def login():
    return authenticate(request.form)


@users_bp.route('/', methods=['GET'])
@check_login
def index():
    return render_template('index.html')


@users_bp.route('/gtAlUsers', methods=['GET'])
@check_login
def gt_al_users():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    return qry_al_users(page, limit)


@users_bp.route('/update', methods=['POST'])
@check_login
def update_usr():
    return update_user(request.form)


@users_bp.route('/del/<int:user_id>', methods=['GET'])
@check_login
def delete_user(user_id):
    return del_usr(user_id)


@users_bp.route('/add', methods=['POST'])
@check_login
def add_user():
    return add_usr(request.form)
