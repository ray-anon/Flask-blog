from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()
DB_NAME = 'Database.db'
def create_app():
    app.config['SECRET_KEY'] = 'elkbrewr32bekf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    from .models import User
    from .views import views
    from .auth import auth
    app.register_blueprint(views , url_prefix="/")
    app.register_blueprint(auth , url_prefix="/")
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    db.init_app(app)
    create_database()

    return app

def create_database():
    with app.app_context():
        db.create_all()