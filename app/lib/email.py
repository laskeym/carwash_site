###########################################
#          Module to send emails          #
###########################################

from app import mail
from flask import render_template
from flask_mail import Message

def email_subscribe(email, password):
    msg = Message('Welcome to Elite Carwash!', recipients=[email])
    msg.html = render_template('email/subscribe.html', email=email, password=password)

    mail.send(msg)
