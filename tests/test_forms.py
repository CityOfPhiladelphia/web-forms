from shared_fixtures import app_fixture, model_fixtures
from utils import json_call, dict_contains, iso_regex

def test_create_form(app_fixture, model_fixtures):
    test_client = app_fixture.test_client()

    response = json_call(test_client.post, '/forms', {
        'name': 'my-form',
        'title': 'My Form',
        'action': 'webhook',
        'action_config': {
            'url': 'https://foo.com/webhook'
        }
    })
    assert response.status_code == 201
    assert dict_contains(response.json, {
        'name': 'my-form',
        'title': 'My Form',
        'description': None,
        'action': 'webhook',
        'forms': [],
        'schema': None,
        'action_config': {'url': 'https://foo.com/webhook'},
        'max_submissions_per_minute': 5,
        'created_at': iso_regex,
        'updated_at': iso_regex
    })

def test_get_form(app_fixture, model_fixtures):
    test_client = app_fixture.test_client()

    response = json_call(test_client.get, '/forms/beta-feedback')
    assert response.status_code == 200
    assert dict_contains(response.json, {
        'name': 'beta-feedback',
        'title': 'Beta Feedback Form',
        'description': None,
        'action': 'webhook',
        'forms': [],
        'schema': None,
        'action_config': {'url': 'https://example.com/webhook'},
        'max_submissions_per_minute': 5,
        'created_at': iso_regex,
        'updated_at': iso_regex
    })

def test_list_forms(app_fixture, model_fixtures):
    test_client = app_fixture.test_client()

    response = json_call(test_client.get, '/forms')
    assert response.status_code == 200
    assert response.json['count'] == 2
    assert response.json['page'] == 1
    assert response.json['total_pages'] == 1
    assert len(response.json['data']) == 2
    assert dict_contains(response.json['data'][0], {
        'name': 'beta-feedback',
        'title': 'Beta Feedback Form',
        'description': None,
        'action': 'webhook',
        'forms': [],
        'schema': None,
        'action_config': {'url': 'https://example.com/webhook'},
        'max_submissions_per_minute': 5,
        'created_at': iso_regex,
        'updated_at': iso_regex
    })
    assert dict_contains(response.json['data'][1], {
        'name': 'parks-contact-us',
        'title': 'Parks and Recreation Contact Us Form',
        'description': 'Primary ontact us form for the Parks and Recreation Department',
        'action': 'store_only',
        'forms': [],
        'schema': None,
        'action_config': None,
        'max_submissions_per_minute': 5,
        'created_at': iso_regex,
        'updated_at': iso_regex
    })

def test_update_form(app_fixture, model_fixtures):
    test_client = app_fixture.test_client()

    response = json_call(test_client.get, '/forms/beta-feedback')
    assert response.status_code == 200

    form = response.json
    form['description'] = 'Form used to get feedback on beta.phila.gov'

    response = json_call(test_client.put, '/forms/beta-feedback', form)
    assert response.status_code == 200
    assert dict_contains(response.json, {
        'name': 'beta-feedback',
        'title': 'Beta Feedback Form',
        'description': 'Form used to get feedback on beta.phila.gov',
        'action': 'webhook',
        'forms': [],
        'schema': None,
        'action_config': {'url': 'https://example.com/webhook'},
        'max_submissions_per_minute': 5,
        'created_at': iso_regex,
        'updated_at': iso_regex
    })
