import os

import pytest

from web_forms.app import app
from web_forms.models import db, Form, FormSubmission

@pytest.fixture
def app_fixture():
    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def model_fixtures(app_fixture):
    with app_fixture.app_context():
        form1 = Form(name='parks-contact-us',
                     title='Parks and Recreation Contact Us Form',
                     description='Primary ontact us form for the Parks and Recreation Department',
                     action='store_only')
        form2 = Form(name='beta-feedback',
                     title='Beta Feedback Form',
                     action='webhook',
                     action_config={'url': 'https://example.com/webhook'})
        db.session.add(form1)
        db.session.add(form2)
        db.session.commit()
