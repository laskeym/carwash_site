import os
import stripe

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  SERVER_NAME = 'localhost:5000'

  # SQLALCHEMY
  SQLALCHEMY_DATABASE_URI = 'sqlite:///{db}'\
            .format(db=os.path.join(basedir, 'app.db'))
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # FLASK-WTF
  RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
  RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

  # Flask-Mail
  MAIL_SERVER = 'smtp.gmail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USE_SSL = False
  MAIL_DEBUG = True
  MAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
  MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_USERNAME')
  MAIL_MAX_EMAILS = None
  MAIL_SUPRESS_SEND = False
  MAIl_ASCII_ATTACHMENTS = False

  # Stripe
  STRIPE_KEYS = {
    'secret_key': os.environ.get('STRIPE_SK'),
    'publishable_key': os.environ.get('STRIPE_PK')
  }

  stripe.api_key = STRIPE_KEYS['secret_key']