import datetime

from app import app, db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)


class UserProfile(db.Model):
  __tablename__ = 'user_profile'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  first_name = db.Column(db.String)
  last_name = db.Column(db.String)
  birth_date = db.Column(db.DateTime)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)



