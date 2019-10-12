import random
from datetime import datetime as dt
from pprint import pformat

from flask import current_app as app
from flask import flash, render_template, url_for
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .utils.password import hash_password
from flask_login import UserMixin

# def update(self, data):
#     for key in data:
#         if data[key] == "":
#             data[key] = None

#         setattr(self, key, data[key])

#     return self

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    fname = db.Column(db.String(128))
    lname = db.Column(db.String(128))
    bio = db.Column(db.Text)
    role = db.Column(db.String(10))
    website = db.Column(db.String(128))
    location = db.Column(db.String(128))
    phone = db.Column(db.String(10))
    dob = db.Column(db.Date)
    profile_image = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, nullable=False)
    date_modified = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean)
    email_confirmed = db.Column(db.Boolean)

    def __init__(self,
                 email,
                 fname,
                 lname,
                 role=None,
                 bio=None,
                 website=None,
                 location=None,
                 phone=None,
                 dob=None,
                 profile_image=None,
                 email_confirmed=False,
                 ):
        self.username = email
        self.email = email

        self.set_password(password)

        self.fname = fname
        self.lname = lname

        self.bio = bio
        self.website = website
        self.location = location
        self.phone = phone
        self.dob = dob

        if role is None:
            self.role = 'user'
        else:
            self.role = role

        profileImages = ['green_default.png', 'blue_default.png',
                         'red_default.png', 'yellow_default.png', 'orange_default.png']

        if profile_image is None:
            self.profile_image = url_for(
                'static', filename='img/' + random.choice(profileImages))
        else:
            self.profile_image = profile_image

        # Default Values
        now = dt.now().isoformat()  # Current Time to Insert into Datamodels
        self.date_created = now
        self.date_modified = now
        self.active = True

        if app.config['TESTING']:
            self.email_confirmed = True
        else:
            self.email_confirmed = email_confirmed

    def __repr__(self):
        return '<User %r | %s(%d)>' % (self.username, self.name, self.id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'fname': self.fname,
            'lname': self.lname,
            'profileImageURL': self.profile_image,
            'url': '/user/view/%d' % self.id
        }

    @property
    def shortSerialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'profileImageURL': self.profile_image,
            'url': '/user/view/%d' % self.id
        }

    # def set_password(self, __password__):
    #     if __password__ == "":
    #         return self

    #     # Hash the password. SHA256
    #     hashedPassword = hash_password(__password__)

    #     # Split the password and the salt
    #     splitPassword = hashedPassword.split(":")

    #     self.password = splitPassword[0]  # Password
    #     self.salt = splitPassword[1]     # Salt

    #     return self


