from datetime import datetime

from restful_ben.test_utils import json_call, login, dict_contains, iso_regex
import requests_mock

from shared_fixtures import app
from constable.models import db, RecoverPasswordRequest, User, Token
from constable import worker

password_recovery_fixture = {
    'email': 'amadonna@exampleemail.com',
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
        assert recover_password_request_instance.email == 'amadonna@exampleemail.com'

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

def test_complete_password_recovery(app):
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

        recover_password_request_instance = db.session.query(RecoverPasswordRequest).first()
        token_instance = db.session.query(Token).first()
        user = db.session.query(User).filter(User.email == password_recovery_fixture['email']).one_or_none()

        assert recover_password_request_instance.status == 'verification_email_sent'
        assert recover_password_request_instance.verification_token_id == str(token_instance.id)
        assert recover_password_request_instance.user_id == user.id

        ## TODO: check that send_notification was called

        response = json_call(test_client.post, '/password-recovery/' + token_instance.token, {
            'password': 'how about me now'
        })

        assert response.status_code == 204

        db.session.refresh(recover_password_request_instance)
        assert recover_password_request_instance.status == 'success'

        db.session.refresh(user)
        assert user.verify_password('how about me now')

        db.session.refresh(token_instance)
        assert isinstance(token_instance.revoked_at, datetime)
