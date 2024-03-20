import logging
from functools import wraps

from flask import Flask, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = b'^\x11\xd7\x9c%\x81\xf5\xfd\xfcEq\x93F \\\xfc\xa2s\x87\x7fC>W\xa6'

print("\033[1m\033[32m" + "请准备好MySQL中名为’test‘的数据库" + "\033[22m\033[39m")
print("请输入MySQL连接地址：（127.0.0.1）")
host = input()
print("请输入端口：（3306）")
port = input()
print("输入登录用户名：")
username = input()
print("输入密码：")
password = input()
# 配置Flask应用和数据库连接
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + username + ':' + password + '@' + host + ':' + port + '/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy()
db.init_app(app)
# 设置日志级别和输出方式
logging.basicConfig(level=logging.DEBUG)


def check_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get('user_info'):
            return redirect(url_for('users.login_user'))
        return func(*args, **kwargs)

    return decorated_function
