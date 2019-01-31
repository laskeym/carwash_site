from app import app
from app.forms import RegistrationForm

from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
      # TODO:
        # Add User to DB
      print('SUBMIT')
    return render_template('register.html', form=form)