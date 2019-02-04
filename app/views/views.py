from app import app, db
from app.forms import RegistrationForm, LoginForm, ProfileForm
from app.models import User, UserProfile, Membership, Subscription

from werkzeug.urls import url_parse
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

import stripe


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for('index'))

    form = RegistrationForm(request.form)
    if form.validate_on_submit():
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
      flash('You are already logged in!')
      return redirect(url_for('index'))

    form = LoginForm(request.form)
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


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    form = ProfileForm(obj=profile)
    if form.validate_on_submit():
        if profile:
            form.populate_obj(profile)
            db.session.commit()
            return redirect(url_for('dashboard'))
        new_profile = UserProfile(user_id=current_user.id, first_name=form.first_name.data,
                                  last_name=form.last_name.data, birth_date=form.birth_date.data,
                                  address_1=form.address_1.data, address_2=form.address_2.data,
                                  city=form.city.data, state=form.state.data,
                                  zip=form.zip.data)
        
        db.session.add(new_profile)
        db.session.commit()
        return 'Profile Created!'
    return render_template('profile.html', form=form)


@app.route('/membership', methods=['GET', 'POST'])
@login_required
def membership():
    memberships = Membership.query.all()

    return render_template('membership.html', memberships=memberships,
                           key=app.config['STRIPE_KEYS']['publishable_key'])


@app.route('/charge', methods=['POST'])
@login_required
def charge():
    membership = Membership.query.filter_by(id=request.form['membership-id']).first()
    # Validate membership

    # Amount in cents
    amount = membership.membership_price

    if not current_user.customer_id:
        customer = stripe.Customer.create(
            email=current_user.email,
            source=request.form['stripeToken']
        )
        current_user.customer_id = customer.id

        plan = stripe.Plan.retrieve(membership.plan_id)
        subscription = stripe.Subscription.create(
            customer=current_user.customer_id,
            items=[
              {
                "plan": plan
              }
            ]
        )

        sub = Subscription(
            user_id=current_user.id,
            subscription_id=subscription.id
        )

        db.session.add(sub)
        db.session.commit()

        print('SUBSCRIBED')

    # charge = stripe.Charge.create(
    #   customer=customer.id,
    #   amount=int(amount*100),
    #   currency='usd',
    #   description='Flask Charge'
    # )

    return render_template('charge.html', amount=membership.membership_price)


@app.route('/home')
@login_required
def home():
  return 'The current user is ' + current_user.email

