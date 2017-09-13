from datetime import datetime

from restful_ben.test_utils import json_call, login, dict_contains, iso_regex
import requests_mock

from shared_fixtures import app
from constable.models import db, Registration, Token, User
from constable import worker

registration_fixture = {
    'user': {
        'first_name': 'Alicia',
        'last_name': 'Florrick',
        'email': 'alicia.florrick@example.com',
        'password': 'correct horse battery staple',
        'mobile_phone': '484-555-5555'
    },
    'recaptcha': 'foobar'
}

def test_registration(app):
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

def test_complete_registration(app):
    test_client = app.test_client()

    with requests_mock.Mocker() as m:
        m.post('https://www.google.com/recaptcha/api/siteverify', json={
            'success': True
        })

        test_client = app.test_client()

        response = json_call(test_client.post, '/registrations', registration_fixture)

        assert response.status_code == 204

    with app.app_context():
        worker.run(db.session, 'test-worker', now=datetime.utcnow())

        registration_instance = db.session.query(Registration).first()
        token_instance = db.session.query(Token).first()

        assert registration_instance.status == 'verification_email_sent'
        assert registration_instance.verification_token_id == str(token_instance.id)

        response = test_client.get('/registrations/confirmations/' + token_instance.token)

        assert response.status_code == 303
        assert response.headers['Location'] == 'http://localhost/login'

        db.session.refresh(registration_instance)
        assert registration_instance.hashed_password == None
        assert registration_instance.status == 'success'

        user_instance = db.session.query(User)\
            .filter(User.email == registration_fixture['user']['email'])\
            .one_or_none()

        input_user = registration_fixture['user']

        assert user_instance.active
        assert user_instance.email == input_user['email']
        assert user_instance.first_name == input_user['first_name']
        assert user_instance.last_name == input_user['last_name']
        assert user_instance.mobile_phone == input_user['mobile_phone']
        assert user_instance.verify_password(input_user['password'])
