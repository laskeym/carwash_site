from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
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
