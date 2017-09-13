import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import INET, UUID
from cryptography.fernet import Fernet
from restful_ben.auth import UserAuthMixin, TokenMixin

from . import config

db = SQLAlchemy()

class BaseMixin(object):
    id = db.Column(db.BigInteger, primary_key=True)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now())
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now(),
                           onupdate=func.now())

class UserBase(UserAuthMixin, BaseMixin, db.Model):
    __abstract__ = True

    # hashed_password - from UserAuthMixin
    # password - property from UserAuthMixin
    email = db.Column(db.String(255))
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    title = db.Column(db.String(128))
    mobile_phone = db.Column(db.String(128))
    profile_image_url = db.Column(db.String(255))

class User(UserBase):
    __tablename__ = 'users'

    active = db.Column(db.Boolean, nullable=False)

    @property
    def is_active(self):
        return self.active

    def __repr__(self):
        return '<User id: {} active {} email: {}>'.format(self.id, \
                                                          self.active, \
                                                          self.email)

class Registration(UserBase):
    __tablename__ = 'registrations'

    ip = db.Column(INET)
    user_agent = db.Column(db.String(8192))
    status = db.Column(db.Enum('new',
                               'processing',
                               'email_already_registered',
                               'verification_email_sent',
                               'retry',
                               'failed',
                               'success',
                               name='registration_statuses'),
                       nullable=False)
    locked_at = db.Column(db.DateTime)
    worker_id = db.Column(db.String(255))
    attempts = db.Column(db.Integer, nullable=False, default=0)
    verification_token_id = db.Column(UUID, db.ForeignKey('tokens.id'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Registration id: {} email: {} status: {}>'.format(self.id, self.email, self.status)

class Token(TokenMixin, db.Model):
    fernet = Fernet(config.TOKEN_SECRET)

class Application(db.Model):
    __tablename__ = 'applications'

    name = db.Column(db.String, primary_key=True) ## TODO: only allow [a-z\-]+
    title = db.Column(db.String)
    description = db.Column(db.String)
    session_support = db.Column(db.Boolean)
    oauth_support = db.Column(db.Boolean)
    ## TODO: ui_origin ? would need to include this in CORS headers
    ## TODO: redirect urls for this app?
    oauth_scopes = db.relationship('OAuthScope',
                                   backref='application',
                                   passive_deletes=True) # required to cascade deletes
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now())
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now(),
                           onupdate=func.now())

class OAuthScope(db.Model):
    __tablename__ = 'oauth_scopes'

    application_name = db.Column(
        db.String,
        db.ForeignKey('applications.name', ondelete='CASCADE'),
        primary_key=True)
    scope = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now())
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now(),
                           onupdate=func.now())
