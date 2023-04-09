import flask
from flask import render_template, redirect
from flask_login import login_user, logout_user, login_required


from data.auth_forms import RegistrationForm, LoginForm
from data.users_model import User
from data import db_session

import logging

blueprint = flask.Blueprint(
    'auth_pages',
    __name__,
    template_folder='templates'
)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            logging.info(f'[auth_pages.py, register] New user {form.login.data} register failed')
            return render_template('registration.html',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            login=form.login.data,
            receiver_email=form.receiver_email.data
        )
        user.set_user_password(form.password.data)
        user.set_mail_app_password(form.app_password.data)
        db_sess.add(user)
        db_sess.commit()
        logging.info(f'[auth_pages.py, register] New user {form.login.data} registered')
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_user_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            logging.info(f'[auth_pages.py, login] User {form.login.data} logged in')
            return redirect('/')
        logging.info(f'[auth_pages.py, login] User {form.login.data} log in failed')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
