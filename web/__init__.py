# web/__init__.py

from flask import Flask
from web.routes import web
from domain.models import User
from config import Config
import openai
from infrastructure.database import db, migrate
from flask_migrate import Migrate
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.register_blueprint(web, url_prefix='/')
    
    app.config.from_object(Config)
    
    openai.api_key = app.config['OPENAI_API_KEY']
    
    db.init_app(app)
    migrate = Migrate(app, db)
        
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
        from . import routes  # Import routes
        
    return app
