from restful_ben.test_utils import json_call, login, dict_contains, iso_regex
import requests_mock

from shared_fixtures import app
from constable.models import db, Registration

registration_fixture = {
    'user': {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jdoe@example.com',
        'password': 'correct horse battery staple',
        'mobile_phone': '484-555-5555'
    },
    'recaptcha': 'foobar'
}

def test_registration_success(app):
    with requests_mock.Mocker() as m:
        m.post('https://www.google.com/recaptcha/api/siteverify', json={
            'success': True
        })

        test_client = app.test_client()

        response = json_call(test_client.post, '/registrations', registration_fixture)

        assert response.status_code == 204

    with app.app_context():
        registration_instance = db.session.query(Registration).first()

        registration_user = registration_fixture['user']

        assert registration_instance.status == 'new'
        assert registration_instance.first_name == registration_user['first_name']
        assert registration_instance.last_name == registration_user['last_name']
        assert registration_instance.email == registration_user['email']
        assert registration_instance.mobile_phone == registration_user['mobile_phone']
        assert registration_instance.verify_password(registration_user['password'])

def test_registration_google_fail(app):
    with requests_mock.Mocker() as m:
        m.post('https://www.google.com/recaptcha/api/siteverify', json={
            'success': False
        })

        test_client = app.test_client()

        response = json_call(test_client.post, '/registrations', registration_fixture)

        assert response.status_code == 400

def test_registration_google_500(app):
    with requests_mock.Mocker() as m:
        m.post('https://www.google.com/recaptcha/api/siteverify', status_code=500)

        test_client = app.test_client()

        response = json_call(test_client.post, '/registrations', registration_fixture)

        assert response.status_code == 500
