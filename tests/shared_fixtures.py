import pytest

from constable.app import app as orig_app
from constable.models import db, User

@pytest.fixture
def app():
    with orig_app.app_context():
        db.create_all()

        ## seed users
        db.session.add(User(active=True, email='amadonna@example.com', password='foo'))
        db.session.add(User(active=True, email='jdoe@example.com', password='icecream'))
        db.session.add(User(active=True, email='kclarkson@example.com', password='icecream'))
        db.session.add(User(active=True, email='whouston@example.com', password='icecream'))
        db.session.commit()

    yield orig_app

    with orig_app.app_context():
        db.drop_all()
