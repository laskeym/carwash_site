from app import app, db
from app.lib.pw_gen import pw_gen
from app.lib.email import email_subscribe
from app.forms import RegistrationForm, LoginForm, ProfileForm, ChangePasswordForm
from app.models import User, UserProfile, Membership, Subscription

from werkzeug.urls import url_parse
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

import stripe

from datetime import datetime


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('account'))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid credentials!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('account')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!')

    return redirect(url_for('login'))


@app.route('/subscriptions')
def subscriptions():
    if current_user.is_authenticated:
        return redirect(url_for('account'))

    plans = sorted(stripe.Plan.list(), key=lambda p: p['created'])

    return render_template('subscriptions.html', plans=plans,
                           key=app.config['STRIPE_KEYS']['publishable_key'])


@app.route('/subscribe', methods=['POST'])
def subscribe():
  """
  Subscribe a new customer to a plan.

  1. Create customer account
  2. Create user in DB
  3. Add subscription to Stripe
  4. Email customer with new account credentials
  """
  stripeToken = request.form['stripeToken']
  plan_id = request.form['plan-id']
  email = request.form['stripeEmail']

  if not stripeToken or not plan_id or not email:
      return 'MISSING PARAMETER'

  # Fetch plan
  plan = stripe.Plan.retrieve(plan_id)

  # Do a check to see if email exists in DB
  account = User.query.filter_by(email=email).first()
  if account:
      flash('Account already exists!')
      return redirect(url_for('login'))

  # Create a customer account
  customer = stripe.Customer.create(
      email=email,
      source=request.form['stripeToken']
  )

  # Create new account in DB
  new_account = User(
      email=email,
      customer_id=customer.id
  )
  password = pw_gen()
  new_account.set_password(password)
  db.session.add(new_account)
  db.session.commit()

  # Add new subscription to Stripe
  subscription = stripe.Subscription.create(
      customer=customer.id,
      items=[
          {
              'plan': plan
          }
      ]
  )

  # Email customer with new account credentials
  email_subscribe(email=email, password=password)

  return render_template('subscribe.html', plan=plan)


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/account/subscription')
@login_required
def account_subscription():
    """
    ------
    Note:
    ------
    
    * During subscription retrieval we use the customers subscriptions value.  If this wasn't a 1 to 1 model (i.e 1 Plan to 1 Product) and was a multiple subscription based model, the nested retrival most likely would not be the right approach. 
    """

    customer = stripe.Customer.retrieve(current_user.customer_id)
    subscription = stripe.Subscription.retrieve(customer['subscriptions']['data'][0]['id'])
    charges = sorted(stripe.Charge.list(customer=customer.id), key=lambda ch: ch['created'])
    upcoming_invoice = stripe.Invoice.upcoming(customer=customer.id)

    for charge in charges:
        charge['created'] = datetime.utcfromtimestamp(charge['created']).strftime('%m/%d/%Y')
    subscription['current_period_end'] = datetime.utcfromtimestamp(subscription['current_period_end']).strftime('%m/%d/%Y')
    if subscription['cancel_at']:
        subscription['cancel_at'] = datetime.utcfromtimestamp(subscription['cancel_at']).strftime('%m/%d/%Y')

    return render_template('account_subscription.html', subscription=subscription,
                           charges=charges,
                           upcoming_invoice=upcoming_invoice,
                           customer=customer)


@app.route('/account/subscription/change')
@login_required
def change_subscription():
    customer = stripe.Customer.retrieve(current_user.customer_id)
    subscription = stripe.Subscription.retrieve(customer['subscriptions']['data'][0]['id'])
    plans = sorted(stripe.Plan.list(), key=lambda p: p['created'])
    plans = list(filter(lambda x: x['id'] != subscription['plan']['id'], plans))

    return render_template('change_subscription.html', plans=plans)


@app.route('/account/subscription/update', methods=['POST'])
@login_required
def update_subscription():
    plan_id = request.form['plan-id']
    customer = stripe.Customer.retrieve(current_user.customer_id)
    subscription = stripe.Subscription.retrieve(customer['subscriptions']['data'][0]['id'])

    stripe.Subscription.modify(subscription['id'],
        items=[{
            'id': subscription['items']['data'][0].id,
            'plan': plan_id
        }])

    flash('Subscription Updated!')

    return redirect(url_for('account_subscription'))


@app.route('/account/subscription/cancel', methods=['POST'])
def cancel_subscription():
    action = request.form['action']
    if not action:
        flash('Missing information!')
        return redirect(url_for('account_subscription'))

    customer = stripe.Customer.retrieve(current_user.customer_id)
    subscription = stripe.Subscription.retrieve(customer['subscriptions']['data'][0]['id'])

    if action == 'cancel':
        subscription.cancel_at_period_end = True
        subscription.save()
        cancel_dt = datetime.utcfromtimestamp(subscription['cancel_at']).strftime('%m/%d/%Y')
        flash('Subscription will be cancelled as of {cancel_dt}!'
              .format(cancel_dt=cancel_dt))
    elif action == 'reactivate':
        subscription.cancel_at_period_end = False 
        subscription.save()
        flash('Subscription has been reactivated!')
    else:
        flash('Missing information!')
        return redirect(url_for('account_subscription'))
        
    return redirect(url_for('account_subscription'))


@app.route('/account/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = UserProfile.query.filter_by(user_id=current_user.id).first()
    form = ProfileForm(obj=profile)
    if form.validate_on_submit():
        if profile:
            form.populate_obj(profile)
            db.session.commit()

            flash('Profile Information has been saved!')
            return redirect(url_for('account'))
        new_profile = UserProfile(user_id=current_user.id, first_name=form.first_name.data,
                                  last_name=form.last_name.data, birth_date=form.birth_date.data,
                                  address_1=form.address_1.data, address_2=form.address_2.data,
                                  city=form.city.data, state=form.state.data,
                                  zip=form.zip.data)
        
        db.session.add(new_profile)
        db.session.commit()
        
        flash('Profile Information has been saved!')
        return redirect(url_for('account'))
    return render_template('profile.html', form=form)


@app.route('/account/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Password updated!')
        return redirect(url_for('account'))
    return render_template('change_password.html', form=form)