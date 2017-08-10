import os

import flask
from flask_restful import Api
from flask_cors import CORS
from cryptography.fernet import Fernet
from restful_ben.auth import AuthStandalone

from .models import db, User, Token
from . import resources

TOKEN_SECRET = os.getenv('TOKEN_SECRET', Fernet.generate_key())
CSRF_SECRET = os.getenv('CSRF_SECRET', Fernet.generate_key())
SQLALCHEMY_DATABASE_URI = os.getenv('CSRF_SECRET', 'postgresql://localhost/auth_service_test')

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db.init_app(app)
api = Api(app)
CORS(app, supports_credentials=True)

## TODO: pass cookie info?

auth = AuthStandalone(
        app=app,
        session=db.session,
        base_model=db.Model,
        user_model=User,
        token_model=Token,
        token_secret=TOKEN_SECRET,
        csrf_secret=CSRF_SECRET)

def apply_session(class_def):
    setattr(class_def, 'session', db.session)

with app.app_context():
    # session
    api.add_resource(auth.session_resource, '/session')

    # users
    api.add_resource(apply_session(resources.UserListResource), '/users')
    api.add_resource(apply_session(resources.UserResource), '/users/<int:instance_id>')

    # tokens
    api.add_resource(apply_session(resources.TokenListResource), '/tokens')
    api.add_resource(apply_session(resources.TokenResource), '/tokens/<int:instance_id>')

    # applications
    api.add_resource(apply_session(resources.ApplicationListResource), '/applications')
    api.add_resource(apply_session(resources.ApplicationResource), '/applications/<instance_id>')
