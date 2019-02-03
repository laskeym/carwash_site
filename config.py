import os
import stripe

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

  # SQLALCHEMY
  SQLALCHEMY_DATABASE_URI = 'sqlite:///{db}'\
            .format(db=os.path.join(basedir, 'app.db'))
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  # FLASK-WTF
  RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
  RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

  # Stripe
  STRIPE_KEYS = {
    'secret_key': os.environ.get('STRIPE_SK'),
    'publishable_key': os.environ.get('STRIPE_PK')
  }

  stripe.api_key = STRIPE_KEYS['secret_key']