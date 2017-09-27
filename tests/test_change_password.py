from restful_ben.test_utils import json_call, login, dict_contains, iso_regex

from constable.models import db, User

from shared_fixtures import app

def test_password_change(app):
    test_client = app.test_client()
    csrf_token = login(test_client, email='amadonna@exampleemail.com', password='foo')

    response = json_call(test_client.put, '/password-change', {
        'current_password': 'foo',
        'new_password': 'buddy holly weezer'
    }, headers={'X-CSRF': csrf_token})

    assert response.status_code == 204

    with app.app_context():
        user = db.session.query(User).filter(User.email == 'amadonna@exampleemail.com').one_or_none()

        assert user.verify_password('buddy holly weezer')
