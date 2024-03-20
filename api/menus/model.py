from sqlalchemy import Column, Integer, String

from api import db
from api.users.models import Users


class Menus(db.Model):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True)
    menu_name = Column(String(20), unique=True, nullable=False)
    uri = Column(String(50), unique=True, nullable=False)
    parent_id = Column(Integer())


class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(15), unique=True, nullable=False)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey(Roles.id), primary_key=True)


class RoleMenus(db.Model):
    __tablename__ = 'role_menus'
    menu_id = db.Column(db.Integer, db.ForeignKey(Menus.id), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey(UserRoles.role_id), primary_key=True)
