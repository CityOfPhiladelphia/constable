import re

from restful_ben.test_utils import json_call, login, dict_contains, iso_regex

from shared_fixtures import app

def test_login(app):
    test_client = app.test_client()

    response = json_call(test_client.post, '/session', username='amadonna', password='foo')

    assert response.status_code == 201
    assert 'csrf_token' in response.json
    assert len(response.json['csrf_token']) > 64
    assert 'Set-Cookie' in response.headers

    cookie_regex = r'session=[^;]+;\sExpires=[A-Za-z]{3},\s[0-9]{2}\s[A-Za-z]{3}\s[0-9]{4}\s[0-9]{2}:[0-9]{2}:[0-9]{2}\sGMT;\sHttpOnly'

    matches = re.match(cookie_regex, response.headers['Set-Cookie'])
    assert matches != None
