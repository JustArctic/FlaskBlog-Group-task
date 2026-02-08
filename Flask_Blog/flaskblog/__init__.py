import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from flaskblog.posts.utils import TAG_LABELS

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def load_admin_user():
        from flaskblog.models import User
        
        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")
        # Check if admin already exists by email 
        admin = User.query.filter_by(email=email).first()
        if not admin:
            admin = User(username=email.split("@")[0], email=email, password = bcrypt.generate_password_hash(password).decode('utf-8'), is_admin=True)
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user with email '{email}' and password '{password}' created.") 
        else: 
            print(f"Admin user with email '{email}' and password '{password}' already exists.")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    @app.context_processor 
    def inject_tag_labels():
        return dict(tag_labels=TAG_LABELS)

    # Create admin user on startup
    with app.app_context(): 
        db.create_all()
        load_admin_user()

    return app