# app/web/routes.py

from flask import render_template, flash, redirect, url_for, request, session, make_response
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from domain.models import User, Idea
from infrastructure.database import db
from web.forms import LoginForm, RegistrationForm, IdeaForm

from flask import Blueprint

web = Blueprint('web', __name__)

@web.route('/')
@web.route('/home')
@login_required
def home():
    return render_template('home.html', title='Home')

@web.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('web.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('web.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('web.home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@web.route('/logout')
def logout():
    logout_user()
    
    #WIP Causing Problems
    #response = make_response("Logging out...")
    #response.set_cookie('session', '', expires=0, path='/')
    #session.clear()
    
    return redirect(url_for('web.login'))

@web.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('web.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('web.login'))
    return render_template('register.html', title='Register', form=form)

@web.route('/idea', methods=['GET', 'POST'])
def new_idea():
    form = IdeaForm()
    if form.validate_on_submit():
        idea = Idea(content=form.content.data, user_id=current_user.id)
        db.session.add(idea)
        db.session.commit()
        return redirect(url_for('web.home'))  # Oder eine andere Zielseite
    return render_template('idea.html', title='New Idea', form=form)