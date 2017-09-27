from restful_ben.test_utils import json_call, login, dict_contains, iso_regex

from shared_fixtures import app, groups_roles_permissions

def test_get_user(app, groups_roles_permissions):
    test_client = app.test_client()
    login(test_client, email='amadonna@exampleemail.com', password='foo')

    response = json_call(test_client.get, '/users/1')

    assert response.status_code == 200
    assert dict_contains(response.json, {
        'id': 1,
        'active': True,
        'email': 'amadonna@exampleemail.com',
        'first_name': None,
        'last_name': None,
        'profile_image_url': None,
        'created_at': iso_regex,
        'updated_at': iso_regex
    })

    response = json_call(test_client.get, '/users/2')

    assert response.status_code == 403
