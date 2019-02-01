from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User

from werkzeug.urls import url_parse
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      flash('You are already logged in!')
      return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid credentials!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!')

    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
  return 'The current user is ' + current_user.email


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
      print(form.data)
      user = User.query.filter_by(email=form.email.data).first()
      if user:
        form.errors['email'] = 'Account with that email already exists!'
        return render_template('register.html', form=form)
      
      user = User(email=form.email.data)
      user.set_password(form.password.data)

      db.session.add(user)
      db.session.commit()
      
      flash('Account created!')
      return redirect(url_for('login'))
    return render_template('register.html', form=form)