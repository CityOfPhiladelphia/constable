import pytest

from constable.app import app as orig_app
from constable.models import db, User

@pytest.fixture
def app():
    with orig_app.app_context():
        db.create_all()

        ## seed users
        db.session.add(User(active=True, username='amadonna', password='foo'))
        db.session.add(User(active=True, username='jdoe', password='icecream'))
        db.session.add(User(active=True, username='kclarkson', password='icecream'))
        db.session.add(User(active=True, username='whouston', password='icecream'))
        db.session.commit()

    yield orig_app

    with orig_app.app_context():
        db.drop_all()
