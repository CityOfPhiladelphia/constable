from restful_ben.auth import (
    csrf_check
)
from restful_ben.resources import (
    RetrieveUpdateDeleteResource,
    QueryEngineMixin,
    CreateListResource
)

from .models import (
    User,
    Token,
    Application
)

## TODO: change password - need to confirm current password as well
## TODO: password recovery

## TODO: /applications/scopes
## TODO: /applications/scopes/:name

class ApplicationSchema(UserSchema):
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

## TODO: authorization - users can edit themselves

class UserSchemaPOST(ModelSchema):
    class Meta:
        model = User
        exclude = ['hashed_password']

    id = field_for(User, 'id', dump_only=True)
    password = fields.Str(load_only=True)
    created_at = field_for(User, 'created_at', dump_only=True)
    updated_at = field_for(User, 'updated_at', dump_only=True)

class UserSchemaPUT(UserSchema):
    class Meta:
        model = User
        exclude = ['hashed_password', 'password']

    id = field_for(User, 'id', dump_only=True)
    username = field_for(User, 'username', dump_only=True)
    created_at = field_for(User, 'created_at', dump_only=True)
    updated_at = field_for(User, 'updated_at', dump_only=True)

user_schema_post = UserSchemaPOST()
user_schema_put = UserSchemaPUT()
users_schema = UserSchema(many=True)

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

class TokenSchema(UserSchema):
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
