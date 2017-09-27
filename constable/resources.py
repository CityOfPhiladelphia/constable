from functools import wraps
import os

from marshmallow import fields, validate, Schema
from marshmallow_sqlalchemy import ModelSchema, field_for
from sqlalchemy import func
from flask import request, current_app
from flask_login import login_required, current_user
from flask_restful import Resource, abort
from zxcvbn import zxcvbn
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
    Registration,
    RecoverPasswordRequest,
    Group,
    Role,
    Resource as ResourceModel,
    Permission,
    get_authorization
)

from .mailchecker import MailChecker

from . import config

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

## groups

class GroupSchema(ModelSchema):
    class Meta:
        model = Group

    id = field_for(Group, 'id', dump_only=True)
    created_at = field_for(Group, 'created_at', dump_only=True)
    updated_at = field_for(Group, 'updated_at', dump_only=True)

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)

class GroupResource(RetrieveUpdateDeleteResource):
    method_decorators = [csrf_check, login_required]

    single_schema = group_schema
    model = Group
    session = db.session

class GroupListResource(QueryEngineMixin, CreateListResource):
    method_decorators = [csrf_check, login_required]

    single_schema = group_schema
    many_schema = groups_schema
    model = Group
    session = db.session

## roles

class RoleSchema(ModelSchema):
    class Meta:
        model = Role

    id = field_for(Role, 'id', dump_only=True)
    created_at = field_for(Role, 'created_at', dump_only=True)
    updated_at = field_for(Role, 'updated_at', dump_only=True)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

class RoleResource(RetrieveUpdateDeleteResource):
    method_decorators = [csrf_check, login_required]

    single_schema = role_schema
    model = Role
    session = db.session

class RoleListResource(QueryEngineMixin, CreateListResource):
    method_decorators = [csrf_check, login_required]

    single_schema = role_schema
    many_schema = roles_schema
    model = Role
    session = db.session

## permissions

class PermissionSchema(ModelSchema):
    class Meta:
        model = Permission

    id = field_for(Permission, 'id', dump_only=True)
    created_at = field_for(Permission, 'created_at', dump_only=True)
    updated_at = field_for(Permission, 'updated_at', dump_only=True)

permission_schema = PermissionSchema()
permissions_schema = PermissionSchema(many=True)

class PermissionResource(RetrieveUpdateDeleteResource):
    method_decorators = [csrf_check, login_required]

    single_schema = permission_schema
    model = Permission
    session = db.session

class PermissionListResource(QueryEngineMixin, CreateListResource):
    method_decorators = [csrf_check, login_required]

    single_schema = permission_schema
    many_schema = permissions_schema
    model = Permission
    session = db.session

## resources

class ResourceSchema(ModelSchema):
    class Meta:
        model = ResourceModel

    created_at = field_for(ResourceModel, 'created_at', dump_only=True)
    updated_at = field_for(ResourceModel, 'updated_at', dump_only=True)

resource_schema = ResourceSchema()
resources_schema = ResourceSchema(many=True)

class ResourceResource(RetrieveUpdateDeleteResource):
    method_decorators = [csrf_check, login_required]

    single_schema = resource_schema
    model = ResourceModel
    session = db.session

class ResourceListResource(QueryEngineMixin, CreateListResource):
    method_decorators = [csrf_check, login_required]

    single_schema = resource_schema
    many_schema = resources_schema
    model = ResourceModel
    session = db.session

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

def user_authorization(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.id == kwargs['instance_id']:
            return func(*args, **kwargs)

        authorization = get_authorization(current_user, 'read', 'users') ## method_to_action(request.method)

        print(authorization)

        if authorization:
            setattr(request, 'authorization', authorization)
            return func(*args, **kwargs)

        abort(403)
    return wrapper

class UserResource(RetrieveUpdateDeleteResource):
    method_decorators = [csrf_check, login_required, user_authorization]
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

class PasswordChangeSchema(Schema):
    current_password = fields.String(required=True, validate=[validate.Length(max=128)])
    new_password = fields.String(required=True, validate=[validate.Length(min=8, max=128)])

password_change_schema = PasswordChangeSchema()

class PasswordChangeResource(Resource):
    session = db.session

    @login_required
    @csrf_check
    def put(self):
        raw_body = request.json
        input_load = password_change_schema.load(raw_body)

        if input_load.errors:
            abort(400, errors=input_load.errors)

        password_change_input = input_load.data

        user = current_user

        if not user or not user.verify_password(password_change_input['current_password']):
            abort(401, errors=['Not Authorized'])

        result = zxcvbn(password_change_input['new_password'], user_inputs=[
            user.email,
            user.first_name,
            user.last_name
        ])

        if result['score'] <= 2:
            abort(400, errors=['Password is too weak'])

        user.password = password_change_input['new_password']
        self.session.commit()

        return None, 204

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

## TODO: don't allow updates on revoked tokens
## TODO: a revoked token / session should not be able to unrevoke itself

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

## reCAPTCHA helper

def verify_recaptcha(recaptcha_code, ip):
    google_request_data = {
        'secret': config.GOOGLE_RECAPTCHA_SECRET,
        'response': recaptcha_code,
        'remoteip': ip
    }

    google_response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data=google_request_data)

    if google_response.status_code != 200:
        current_app.logger.error('Non-200 response from Google reCAPTCHA')
        abort(500)

    google_response_data = google_response.json()

    if google_response_data['success'] != True:
        abort(400, errors=['Bad Request'])

    ## TODO: make sure google_response_data['challenge_ts'] is not to far off
    ## TODO: verify google_response_data['hostname']
    ## TODO: inspect google_response_data['error-codes'] ?

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
        input_load = registration_schema.load(raw_body)

        if input_load.errors:
            abort(400, errors=input_load.errors)

        registration = input_load.data

        result = zxcvbn(registration['user']['password'], user_inputs=[
            registration['user']['email'],
            registration['user']['first_name'],
            registration['user']['last_name']
        ])

        if result['score'] <= 2:
            abort(400, errors=['Password is too weak'])

        if not MailChecker.is_valid_email_format(registration['user']['email']):
            abort(400, errors=['Email is invalid'])

        if MailChecker.is_blacklisted(registration['user']['email']):
            abort(400, errors=['Cannot use disposable email address'])

        ip = get_ip(config.NUMBER_OF_PROXIES)

        verify_recaptcha(registration['recaptcha'], ip)

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

        token.revoked_at = func.now()

        self.session.commit()

        return None, 303, {'Location': '{}/login'.format(config.BASE_URL)}

## Password Recovery

class RecoverPasswordRequestSchema(Schema):
    email = fields.String(required=True, validate=[validate.Length(max=255)])
    recaptcha = fields.String(required=True, validate=[validate.Length(max=512)])

recovery_password_request_schema = RecoverPasswordRequestSchema()

class RecoverPasswordRequestResource(Resource):
    session = db.session

    def post(self):
        raw_body = request.json
        input_load = recovery_password_request_schema.load(raw_body)

        if input_load.errors:
            abort(400, errors=input_load.errors)

        recover_password_input = input_load.data

        ip = get_ip(config.NUMBER_OF_PROXIES)

        verify_recaptcha(recover_password_input['recaptcha'], ip)

        recover_password_request = RecoverPasswordRequest(
            email=recover_password_input['email'],
            ip=ip,
            user_agent=request.user_agent.string,
            status='new')

        self.session.add(recover_password_request)
        self.session.commit()

        return None, 204

class RecoverPasswordSchema(Schema):
    password = fields.String(required=True, validate=[validate.Length(min=8, max=128)])

recovery_password_schema = RecoverPasswordSchema()

class RecoverPasswordResource(Resource):
    session = db.session

    def post(self, token_str):
        token = Token.verify_token(self.session, token_str)

        if token == None or token.scopes == None or 'password_recovery' not in token.scopes:
            abort(401, errors=['Not Authorized'])

        raw_body = request.json
        input_load = recovery_password_schema.load(raw_body)

        if input_load.errors:
            abort(400, errors=input_load.errors)

        recover_password_request = self.session.query(RecoverPasswordRequest)\
            .filter(RecoverPasswordRequest.verification_token_id == str(token.id))\
            .one_or_none()

        if not recover_password_request:
            abort(401, errors=['Not Authorized'])

        recover_password_input = input_load.data

        user = self.session.query(User).filter(User.id == recover_password_request.user_id).one_or_none()

        if not user:
            abort(401, errors=['Not Authorized'])

        result = zxcvbn(recover_password_input['password'], user_inputs=[
            user.email,
            user.first_name,
            user.last_name
        ])

        if result['score'] <= 2:
            abort(400, errors=['Password is too weak'])

        user.password = recover_password_input['password']
        recover_password_request.status = 'success'
        token.revoked_at = func.now()

        self.session.commit()

        return None, 204
