from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms import validators


class RegistrationForm(FlaskForm):
    email = EmailField('Email Address', [validators.DataRequired(),
                                         validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.Length(min=8),
                                          validators.EqualTo('password2', message='Passwords must match!')])
    password2 = PasswordField('Repeat Password')
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField('Email Address', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class ProfileForm(FlaskForm):
    choices = [('nj', 'NJ'), ('ny', 'NY'), ('pa', 'PA'), ('ct', 'CT')]

    first_name = StringField()
    last_name = StringField()
    birth_date = DateField()
    address_1 = StringField()
    address_2 = StringField()
    city = StringField()
    state = SelectField(choices=choices)
    zip = StringField()
    submit = SubmitField('Submit')