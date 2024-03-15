import uuid

from flask import jsonify, session, redirect, url_for
from sqlalchemy import func
from sqlalchemy.orm import aliased

from api import db
from api.menus.model import UserRoles, Roles
from api.users.models import Users


def login_user(username, password, role_id):
    try:
        # 或者在密码已加密的情况下，查询后解密比对（实际情况应使用哈希和盐值比较）
        user, role = db.session.query(Users, Roles).join(
            (UserRoles, Users.id == UserRoles.user_id)).filter(
            Users.username == username).filter(UserRoles.role_id == role_id).filter(Roles.id == UserRoles.role_id).one()
        if password == user.password:
            return user, role
    except Exception as e:
        return None, e


def authenticate(data):
    username = data.get('username')
    password = data.get('password')
    role_id = data.get('role')
    user, role = login_user(username, password, int(role_id))
    if user:
        # 将用户信息存储在session中
        session['user_info'] = user.to_dict(role)
        return redirect(url_for('users.index'))
    else:
        # 登录失败
        return jsonify({"status": "error", "message": role.args[0]}), 401


def qry_al_users(page, limit):
    # 根据某种排序进行分页查询
    u = aliased(Users)
    usr_rls = aliased(UserRoles)
    roles = aliased(Roles)
    query = db.session.query(u.id, u.username, u.email, u.age, u.gender, u.registration_date, u.last_login,
                             roles.role_name, roles.id.label('role_id'))
    query = query.join(usr_rls, u.id == usr_rls.user_id).join(roles, usr_rls.role_id == roles.id)
    query = query.filter(usr_rls.role_id > session.get("user_info")['role_id']).order_by(u.id.desc())
    result = [dict(row) for row in query.limit(limit).offset((page - 1) * limit).all()]
    return jsonify({"status": "success", 'code': 0, 'data': result, 'count': len(query.all())}), 200


def update_user(form):
    user = Users.query.filter_by(id=form.get("id")).first()
    user.username = form.get("username")
    user.email = form.get("email")
    user.age = form.get("age")
    user.gender = form.get("gender")
    db.session.commit()
    return jsonify({"status": "success", 'code': 0}), 200


def del_usr(user_id):
    user = Users.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"status": "success", 'code': 0}), 200


def add_usr(form):
    new_user = Users()
    new_user.username = form.get("username")
    new_user.password = uuid.uuid4()
    new_user.email = form.get("email")
    new_user.age = form.get("age")
    new_user.gender = "Male" if form.get("gender") == 1 else "Female"
    new_user.registration_date = func.now()
    new_user.is_active = 0
    db.session.add(new_user)
    db.session.commit()
    print(new_user.id)
    return jsonify({"status": "success", 'code': 0, "user_id": new_user.id}), 200
