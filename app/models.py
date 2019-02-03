import datetime

from app import app, db, login_manager

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    membership_id = db.Column(db.Integer, db.ForeignKey('membership.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    membership = db.relationship('Membership', backref='membership')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class UserProfile(db.Model):
  __tablename__ = 'user_profile'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  first_name = db.Column(db.String)
  last_name = db.Column(db.String)
  birth_date = db.Column(db.DateTime)
  address_1 = db.Column(db.String)
  address_2 = db.Column(db.String)
  city = db.Column(db.String)
  state = db.Column(db.String(2))
  zip = db.Column(db.String)


class Membership(db.Model):
    __tablename__ = 'membership'

    id = db.Column(db.Integer, primary_key=True)
    membership_name = db.Column(db.String, nullable=False)
    membership_description = db.Column(db.String)
    membership_price = db.Column(db.Float(), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)



