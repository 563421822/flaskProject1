from flask import jsonify
from sqlalchemy.orm import aliased

from api import db
from api.menus.model import Menus, RoleMenus, UserRoles
from api.utils.dic_util import model_to_dict


def get_menus(userid):
    menu = aliased(Menus)
    user_roles = aliased(UserRoles)
    role_menus = aliased(RoleMenus)
    query = db.session.query(menu)
    query = query.join((role_menus, menu.id == role_menus.menu_id))
    query = query.join((user_roles, role_menus.role_id == user_roles.role_id))
    query = query.filter(user_roles.user_id == int(userid))
    results = [model_to_dict(row) for row in query.all()]
    l: list = []
    for menu in results:
        c: list = []
        for m in results:
            if m['parent_id'] == menu['id']:
                c.append(m)
        obj = {'menu_id': menu['id'], 'menu_name': menu['menu_name'], 'uri': menu['uri'],
               'parent_id': menu['parent_id'], 'childNode': c}
        l.append(obj)
    return jsonify(l)
