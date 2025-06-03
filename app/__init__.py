from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import routes as auth_routes
    from .users import routes as user_routes
    from .lists import routes as list_routes
    from .tasks import routes as task_routes

    app.register_blueprint(auth_routes.auth_bp)
    app.register_blueprint(user_routes.user_bp)
    app.register_blueprint(list_routes.list_bp)
    app.register_blueprint(task_routes.task_bp)

    with app.app_context():
        db.create_all()

    return app
