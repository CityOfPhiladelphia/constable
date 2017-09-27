import pytest

from constable.app import app as orig_app
from constable.models import (
    db,
    User,
    Group,
    GroupMembership,
    Role,
    RoleAssignment,
    Permission,
    Resource
)

@pytest.fixture
def app():
    with orig_app.app_context():
        db.create_all()

        ## seed users
        db.session.add(User(active=True, email='amadonna@exampleemail.com', password='foo'))
        db.session.add(User(active=True, email='jdoe@exampleemail.com', password='icecream'))
        db.session.add(User(active=True, email='kclarkson@exampleemail.com', password='icecream'))
        db.session.add(User(active=True, email='whouston@exampleemail.com', password='icecream'))
        db.session.commit()

    yield orig_app

    with orig_app.app_context():
        db.drop_all()

@pytest.fixture
def groups_roles_permissions(app):
    with orig_app.app_context():
        group1 = Group(title='ODDT Admins')
        db.session.add(group1)

        role1 = Role(title='Auth Admin')
        db.session.add(role1)

        permission1 = Permission(title='Read User',
                                 action='read',
                                 resource_name='users',
                                 resource_query='*',
                                 fields='*')
        db.session.add(permission1)

        user_resource = Resource(name='users')
        db.session.add(user_resource)

        db.session.commit()

        user = db.session.query(User).get(1)

        db.session.add(GroupMembership(parent_id=group1.id, member_type='user', member_id=user.id))
        db.session.add(RoleAssignment(role_id=role1.id, principle_type='group', principle_id=group1.id))
        role1.permissions.append(permission1)

        db.session.commit()
