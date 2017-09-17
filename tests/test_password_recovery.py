from restful_ben.test_utils import json_call, login, dict_contains, iso_regex
import requests_mock

from shared_fixtures import app
from constable.models import db, RecoverPasswordRequest
from constable import worker

password_recovery_fixture = {
    'email': 'alicia.florrick@example.com',
    'recaptcha': 'foo'
}

def test_recovery_request(app):
    with requests_mock.Mocker() as m:
        m.post('https://www.google.com/recaptcha/api/siteverify', json={
            'success': True
        })

        test_client = app.test_client()

        response = json_call(test_client.post, '/password-recovery', password_recovery_fixture)

        assert response.status_code == 204

    with app.app_context():
        recover_password_request_instance = db.session.query(RecoverPasswordRequest).first()

        assert recover_password_request_instance.status == 'new'
        assert recover_password_request_instance.email == 'alicia.florrick@example.com'

def test_recovery_request_google_fail(app):
    with requests_mock.Mocker() as m:
        m.post('https://www.google.com/recaptcha/api/siteverify', json={
            'success': False
        })

        test_client = app.test_client()

        response = json_call(test_client.post, '/password-recovery', password_recovery_fixture)

        assert response.status_code == 400

def test_recovery_request_google_500(app):
    with requests_mock.Mocker() as m:
        m.post('https://www.google.com/recaptcha/api/siteverify', status_code=500)

        test_client = app.test_client()

        response = json_call(test_client.post, '/password-recovery', password_recovery_fixture)

        assert response.status_code == 500

def test_complete_registration(app):
    test_client = app.test_client()

    with requests_mock.Mocker() as m:
        m.post('https://www.google.com/recaptcha/api/siteverify', json={
            'success': True
        })

        test_client = app.test_client()

        response = json_call(test_client.post, '/password-recovery', password_recovery_fixture)

        assert response.status_code == 204

    with app.app_context():
        worker.run(db.session, 'test-worker', now=datetime.utcnow())
