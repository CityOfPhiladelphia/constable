from flask_sqlalchemy import SQLAlchemy
from restful_ben.auth import UserAuthMixin, TokenMixin

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

class User(UserAuthMixin, BaseMixin, db.Model):
    __tablename__ = 'users'

    # username - from UserAuthMixin
    # hashed_password - from UserAuthMixin
    # password - property from UserAuthMixin
    active = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    display_name = db.Column(db.String)
    title = db.Column(db.String)
    profile_image_url = db.Column(db.String)

    @property
    def is_active(self):
        return self.active

    def __repr__(self):
        return '<User id: {} active {} username: {} email: {}>'.format(self.id, \
                                                                       self.active, \
                                                                       self.username, \
                                                                       self.email)

class Token(TokenMixin, db.Model):
    pass

class Application(BaseMixin, db.Model):
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
        db.ForeignKey('applications.id', ondelete='CASCADE'),
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
