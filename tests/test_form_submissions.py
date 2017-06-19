from shared_fixtures import app_fixture, model_fixtures
from utils import json_call, dict_contains, iso_regex

from web_forms import resources

class MockGoogleResponse(object):
    def __init__(self, success=True, status_code=200):
        self.success = success
        self.status_code = status_code

    def json(self):
        return {
            'success': self.success
        }

## TODO: test google 500
## TODO: test google success=False
## TODO: test google challenge_ts
## TODO: test google hostname ?
## TODO: test exceeding max_submissions_per_minute

def test_submit_form(app_fixture, model_fixtures, monkeypatch):
    mock_google_response = MockGoogleResponse()
    def mock_google_recaptcha(data):
        return mock_google_response
    monkeypatch.setattr(resources, 'google_recaptcha', mock_google_recaptcha)
    test_client = app_fixture.test_client()

    response = json_call(test_client.post, '/forms/beta-feedback/submissions', {
        'recaptcha': 'somerandomslug',
        'what_happened': 'I have a suggestion or idea.',
        'tell_us_more': 'Have more pictures of puppies.'
    })
    assert response.status_code == 204

    response = json_call(test_client.get, '/submissions?form_name=beta-feedback')
    assert response.status_code == 200
    assert response.json['count'] == 1
    assert response.json['page'] == 1
    assert response.json['total_pages'] == 1
    assert len(response.json['data']) == 1
    assert dict_contains(response.json['data'][0], {
        'id': 1,
        'form': 'beta-feedback', ## TODO: form vs form_name ?
        'status': 'submitted',
        'data': {
            'tell_us_more': 'Have more pictures of puppies.',
            'what_happened': 'I have a suggestion or idea.'
        },
        'referrer': None,
        'user_agent': 'werkzeug/0.12.2',
        'ip': '127.0.0.1',
        'worker_id': None,
        'locked_at': None,
        'retry_delay': 300,
        'timeout': 600,
        'attempts': 0,
        'max_attempts': 1,
        'created_at': iso_regex,
        'updated_at': iso_regex
    })
