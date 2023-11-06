# app/application/auth.py

from flask_login import LoginManager
from domain.models import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
