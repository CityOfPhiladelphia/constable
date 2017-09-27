import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, BigInteger, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import INET, UUID, JSONB
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr, AbstractConcreteBase
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
    ## TODO: add created_by and updated_by ???
    # created_by = db.Column(db.Integer, nullable=False)
    # updated_by = db.Column(db.Integer, nullable=False)

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

    @property
    def is_authenticated(self):
        return isinstance(getattr(self, 'token', None), Token)

    def __repr__(self):
        return '<User id: {} active {} email: {}>'.format(self.id, \
                                                          self.active, \
                                                          self.email)

async_request_statuses = ['new',
                          'processing',
                          'retry',
                          'failed',
                          'success']

class AsyncRequestMixin(object):
    ip = db.Column(INET)
    user_agent = db.Column(db.String(8192))
    ## create a status field with new, processing, retry, failed,
    ## success, and any other status it could be in
    locked_at = db.Column(db.DateTime)
    worker_id = db.Column(db.String(255))
    attempts = db.Column(db.Integer, nullable=False, default=0)

class Registration(AsyncRequestMixin, UserBase):
    __tablename__ = 'registrations'

    status = db.Column(db.Enum(*(async_request_statuses +
                                 ['email_already_registered', 'verification_email_sent']),
                               name='registration_statuses'),
                       nullable=False)
    verification_token_id = db.Column(UUID, db.ForeignKey('tokens.id'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<Registration id: {} email: {} status: {}>'.format(self.id, self.email, self.status)

class RecoverPasswordRequest(AsyncRequestMixin, BaseMixin, db.Model):
    __tablename__ = 'recover_password_requests'

    email = db.Column(db.String(128))
    status = db.Column(db.Enum(*(async_request_statuses +
                                 ['email_does_not_exist',
                                  'verification_email_sent']),
                               name='recover_password_request_statuses'),
                       nullable=False)
    verification_token_id = db.Column(UUID, db.ForeignKey('tokens.id'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<RecoverPasswordRequest id: {} email: {} status: {}>'.format(self.id, self.email, self.status)

class Token(TokenMixin, db.Model):
    fernet = Fernet(config.TOKEN_SECRET)

    type = db.Column(db.Enum('session',
                             'token',
                             'refresh_token',
                             'partial_login', ## ?????? other options nfactor
                             name='token_type'),
                     nullable=False)

    def __repr__(self):
        return '<Token id: {} type: {} revoked_at: {} user_id: {}>'.format(self.id, self.type, self.revoked_at, self.user_id)

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

    def __repr__(self):
        return '<Application id: {} name: {}>'.format(self.id, self.name)

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

    def __repr__(self):
        return '<OAuthScope application_name: {} scope: {}>'.format(self.application_name, self.scope)

class GroupMembership(BaseMixin, db.Model):
    __tablename__ = 'group_memberships'

    parent_id = db.Column(db.BigInteger, ForeignKey('groups.id'), nullable=False)
    member_type = db.Column(db.Enum('user','group', name='group_member_types'), nullable=False)
    member_id = db.Column(db.BigInteger, nullable=False)

class Group(BaseMixin, db.Model):
    __tablename__ = 'groups'

    title = db.Column(db.String)
    description = db.Column(db.String)
    member_groups = db.relationship('Group',
                                    secondary=lambda: GroupMembership.__table__,
                                    primaryjoin='GroupMembership.parent_id == Group.id',
                                    secondaryjoin='and_(Group.id == GroupMembership.member_id, ' + 
                                                       'GroupMembership.member_type == "group")',
                                    viewonly=True)
    member_users = db.relationship('User',
                                   secondary=lambda: GroupMembership.__table__,
                                   primaryjoin='GroupMembership.parent_id == Group.id',
                                   secondaryjoin='and_(User.id == GroupMembership.member_id, ' + 
                                                      'GroupMembership.member_type == "user")',
                                   viewonly=True)
    roles = db.relationship('Role',
                            secondary=lambda: RoleAssignment.__table__,
                            primaryjoin='and_(Group.id == RoleAssignment.principle_id, ' + 
                                             'RoleAssignment.principle_type == "group")',
                            secondaryjoin='RoleAssignment.role_id == Role.id',
                            backref='groups',
                            viewonly=True)

class RoleAssignment(BaseMixin, db.Model):
    __tablename__ = 'role_assignments'

    role_id = db.Column(db.BigInteger, ForeignKey('roles.id'))
    principle_type = db.Column(db.Enum('user',
                                       'group',
                                       name='role_principle_types'),
                               nullable=False)
    principle_id = db.Column(db.BigInteger, nullable=False)

roles_permissions_table = Table('roles_permissions', db.Model.metadata,
    Column('role_id', BigInteger, ForeignKey('roles.id')),
    Column('permission_id', BigInteger, ForeignKey('permissions.id'))
)

class Role(BaseMixin, db.Model):
    __tablename__ = 'roles'

    title = db.Column(db.String)
    description = db.Column(db.String)
    permissions = db.relationship('Permission', secondary=roles_permissions_table, backref='roles')

class Permission(BaseMixin, db.Model):
    __tablename__ = 'permissions'

    title = db.Column(db.String)
    description = db.Column(db.String)
    action = db.Column(db.Enum('create',
                               'read',
                               'list',
                               'update',
                               'delete',
                               name='permission_actions'),
                       nullable=False)
    resource_name = db.Column(db.String, ForeignKey('resources.name'), nullable=False)
    resource_query = db.Column(JSONB, nullable=False)
    fields = db.Column(JSONB, nullable=False)

    def __repr__(self):
        return '<Permission id: {} title: {} action: {} resource_name: {}>'.format(self.id, \
                                                                                   self.title, \
                                                                                   self.action, \
                                                                                   self.resource_name)

class Resource(db.Model):
    __tablename__ = 'resources'

    name = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    schema_url = db.Column(db.String)
    schema = db.Column(JSONB)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now())
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now(),
                           onupdate=func.now())

## TODO: prevent cyclical recursion

def get_authorization(user, action, resource):
    print('get_authorization')
    sql = """
        WITH RECURSIVE cte AS (
           SELECT group_memberships.parent_id AS current_group_id FROM group_memberships
           WHERE group_memberships.member_type = 'user' AND group_memberships.member_id = :user_id

           UNION ALL

           SELECT group_memberships.parent_id AS current_group_id
           FROM cte
           JOIN group_memberships
           ON group_memberships.member_type = 'group' AND group_memberships.member_id = cte.current_group_id
        )

        SELECT permissions.* FROM permissions
        JOIN roles_permissions
        ON roles_permissions.permission_id = permissions.id
        JOIN role_assignments
        ON roles_permissions.role_id = role_assignments.role_id
        WHERE
           (role_assignments.principle_type = 'user' AND role_assignments.principle_id = :user_id) OR
           (role_assignments.principle_type = 'group' AND role_assignments.principle_id IN (SELECT DISTINCT current_group_id FROM cte))
           AND permissions.action = :action AND permissions.resource_name = :resource
    """

    ## TODO: dedup permissions in statement? GROUP BY permissios.id?

    try:
        permissions = db.session.query(Permission)\
            .from_statement(text(sql))\
            .params(user_id=user.id, action=action, resource=resource)\
            .all()

        print(permissions)

        if len(permissions) == 0:
            return False

        all_resource = False
        all_fields = False
        or_query = []
        fields = []
        for permission in permissions:
            if permission.resource_query == '*':
                all_resource = True
            else:
                or_query.append(permission.resource_query)

            if permission.fields == '*':
                all_fields = True
            else:
                fields += permission.fields

        resource_query = {'$or': or_query}
    except Exception as e:
        print(e)

    return {
        'fields': '*' if all_fields else fields,
        'resource_query': '*' if all_resource else resource_query
    }
