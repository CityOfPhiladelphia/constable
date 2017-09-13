import os

from marshmallow import fields, validate, Schema
from marshmallow_sqlalchemy import ModelSchema, field_for
from flask import request, current_app
from flask_login import login_required
from flask_restful import Resource, abort
from restful_ben.auth import (
    get_ip,
    csrf_check
)
from restful_ben.resources import (
    RetrieveUpdateDeleteResource,
    QueryEngineMixin,
    CreateListResource
)
import requests

from .models import (
    db,
    User,
    Token,
    Application,
    Registration
)

from . import config

## TODO: change password - need to confirm current password as well
## TODO: password recovery

## TODO: /applications/scopes
## TODO: /applications/scopes/:name

class ApplicationSchema(ModelSchema):
    class Meta:
        model = Application

    created_at = field_for(Application, 'created_at', dump_only=True)
    updated_at = field_for(Application, 'updated_at', dump_only=True)

class ApplicationSchemaPUT(ApplicationSchema):
    name = field_for(Application, 'name', dump_only=True)

appliction_schema = ApplicationSchema()
appliction_schema_put = ApplicationSchemaPUT()
applictions_schema = ApplicationSchema(many=True)

class ApplicationResource(RetrieveUpdateDeleteResource):
    method_decorators = [csrf_check, login_required]

    single_schema = appliction_schema_put
    model = Application
    session = db.session

class ApplicationListResource(QueryEngineMixin, CreateListResource):
    method_decorators = [csrf_check, login_required]

    single_schema = appliction_schema
    many_schema = applictions_schema
    model = Application
    session = db.session

## TODO: /otp - generate seed and only display on POST
## TODO: /otp/:id
## TODO: /otp/verification

## TODO: /groups
## TODO: /groups/:id
## TODO: /roles
## TODO: /roles/:id
## TODO: /permissions
## TODO: /permissions/:id

## TODO: /log

## TODO: /session OTP handshake - return code to exchange for session or mark session as not complete?

######## User

## TODO: authorization - users can view themselves
## TODO: authorization - users can edit themselves

class UserSchemaPOST(ModelSchema):
    class Meta:
        model = User
        exclude = ['hashed_password']

    id = field_for(User, 'id', dump_only=True)
    password = fields.Str(load_only=True)
    created_at = field_for(User, 'created_at', dump_only=True)
    updated_at = field_for(User, 'updated_at', dump_only=True)

class UserSchemaPUT(ModelSchema):
    class Meta:
        model = User
        exclude = ['hashed_password', 'password']

    id = field_for(User, 'id', dump_only=True)
    created_at = field_for(User, 'created_at', dump_only=True)
    updated_at = field_for(User, 'updated_at', dump_only=True)

user_schema_post = UserSchemaPOST()
user_schema_put = UserSchemaPUT()
users_schema = UserSchemaPOST(many=True)

class UserResource(RetrieveUpdateDeleteResource):
    method_decorators = [csrf_check, login_required]
    methods = ['GET', 'PUT']

    single_schema = user_schema_put
    model = User
    session = db.session

class UserListResource(QueryEngineMixin, CreateListResource):
    method_decorators = [csrf_check, login_required]

    query_engine_exclude_fields = ['hashed_password', 'password']
    single_schema = user_schema_post
    many_schema = users_schema
    model = User
    session = db.session

######## Token

## TODO: authorization - users can create API tokens?
## TODO: authorization - users can view their tokens - eg view active sessions and tokens

class TokenSchema(ModelSchema):
    class Meta:
        model = Token

    id = field_for(Token, 'id', dump_only=True)
    type = field_for(Token, 'type', dump_only=True)
    user_id = field_for(Token, 'user_id', dump_only=True)
    created_at = field_for(Token, 'created_at', dump_only=True)
    updated_at = field_for(Token, 'updated_at', dump_only=True)

## TODO: expires_at validation?
## TODO: ip and user_agent set by request? not allowed for non-session tokens?
## TODO: don't allow updates on revoked tokens

token_schema = TokenSchema()
tokens_schema = TokenSchema(many=True)

class TokenResource(RetrieveUpdateDeleteResource):
    method_decorators = [csrf_check, login_required]
    methods = ['GET', 'DELETE']

    single_schema = token_schema
    model = Token
    session = db.session

class TokenListResource(QueryEngineMixin, CreateListResource):
    method_decorators = [csrf_check, login_required]

    single_schema = token_schema
    many_schema = tokens_schema
    model = Token
    session = db.session

## Registration

class RegistrationUserSchema(Schema):
    first_name = fields.String(required=True, validate=[validate.Length(min=2, max=128)])
    last_name = fields.String(required=True, validate=[validate.Length(min=2, max=128)])
    email = fields.String(required=True, validate=[validate.Length(max=255)])
    password = fields.String(required=True, validate=[validate.Length(min=8, max=128)])
    mobile_phone = fields.String(required=True, validate=[validate.Length(max=128)])

class RegistrationSchema(Schema):
    user = fields.Nested(RegistrationUserSchema)
    recaptcha = fields.String(required=True, validate=[validate.Length(max=512)])

registration_schema = RegistrationSchema()

class RegistrationResource(Resource):
    session = db.session

    def post(self):
        raw_body = request.json
        instance_load = registration_schema.load(raw_body)

        if instance_load.errors:
            abort(400, errors=instance_load.errors)

        registration = instance_load.data

        ## TODO: check password strength
        ## TODO: check for temp email
        ## ^ these should be checked on user edit as well

        ip = get_ip(config.NUMBER_OF_PROXIES)

        google_request_data = {
            'secret': config.GOOGLE_RECAPTCHA_SECRET,
            'response': registration['recaptcha'],
            'remoteip': ip
        }

        google_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data=google_request_data)

        print(google_response)
        print(google_response.text)

        if google_response.status_code != 200:
            current_app.logger.error('Non-200 response from Google reCAPTCHA')
            abort(500)

        google_response_data = google_response.json()

        if google_response_data['success'] != True:
            abort(400, errors=['Bad Request'])

        ## TODO: make sure google_response_data['challenge_ts'] is not to far off
        ## TODO: verify google_response_data['hostname']
        ## TODO: inspect google_response_data['error-codes'] ?

        registration_instance = Registration(
            ip=ip,
            user_agent=request.user_agent.string,
            status='new',
            **registration['user']
        )

        self.session.add(registration_instance)
        self.session.commit()

        return None, 204

class RegistrationConfirmationResource(Resource):
    session = db.session

    def get(self, token_str):
        token = Token.verify_token(self.session, token_str)

        if token == None:
            abort(401, errors=['Not Authorized'])

        registration = self.session.query(Registration)\
            .filter(Registration.verification_token_id == str(token.id))\
            .one_or_none()

        if registration == None:
            abort(401, errors=['Not Authorized'])

        user = User(
            active=True,
            email=registration.email,
            hashed_password=registration.hashed_password,
            first_name=registration.first_name,
            last_name=registration.last_name,
            title=registration.title,
            mobile_phone=registration.mobile_phone,
            profile_image_url=registration.profile_image_url)
        self.session.add(user)

        registration.hashed_password = None
        registration.status = 'success'

        self.session.commit()

        return None, 303, {'Location': '{}/login'.format(config.BASE_URL)}
