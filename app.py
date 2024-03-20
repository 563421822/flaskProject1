from api import app, db
from api.books.routes import books_bp
from api.lending.routes import lending_bp
from api.menus.routes import menus_bp
from api.users.routes import users_bp

# 在应用对象上注册蓝图
app.register_blueprint(users_bp)
app.register_blueprint(menus_bp)
app.register_blueprint(books_bp)
app.register_blueprint(lending_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
