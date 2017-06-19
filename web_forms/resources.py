import os

from flask import request
from flask_restful import Resource, abort
from marshmallow_sqlalchemy import ModelSchema, field_for
from flask_login import login_required
import requests
from restful_ben.auth import (
    UserAuthMixin,
    SessionResource,
    authorization,
    CSRF
)
from restful_ben.resources import (
    BaseResource,
    RetrieveUpdateDeleteResource,
    QueryEngineMixin,
    CreateListResource
)

from web_forms.models import db, Form, FormSubmission

GOOGLE_RECAPTCHA_SECRET = os.getenv('GOOGLE_RECAPTCHA_SECRET')

csrf = CSRF()

## Form Resource

class FormSchema(ModelSchema):
    class Meta:
        model = Form

    created_at = field_for(Form, 'created_at', dump_only=True)
    updated_at = field_for(Form, 'updated_at', dump_only=True)

form_schema = FormSchema()
forms_schema = FormSchema(many=True)

form_authorization = authorization({
    'normal': ['GET'],
    'admin': ['POST','PUT','GET','DELETE']
})

class FormResource(RetrieveUpdateDeleteResource):
    #method_decorators = [csrf.csrf_check, form_authorization, login_required]
    single_schema = form_schema
    model = Form
    session = db.session

class FormListResource(QueryEngineMixin, CreateListResource):
    #method_decorators = [csrf.csrf_check, form_authorization, login_required]
    single_schema = form_schema
    many_schema = forms_schema
    model = Form
    session = db.session

## Form Submission

class FormSubmissionSchema(ModelSchema):
    class Meta:
        model = FormSubmission

    id = field_for(FormSubmission, 'id', dump_only=True)
    created_at = field_for(FormSubmission, 'created_at', dump_only=True)
    updated_at = field_for(FormSubmission, 'updated_at', dump_only=True)

form_schema = FormSubmissionSchema()
forms_schema = FormSubmissionSchema(many=True)

form_authorization = authorization({
    'normal': ['POST', 'GET'],
    'admin': ['POST','PUT','GET','DELETE']
})

class FormSubmissionResource(RetrieveUpdateDeleteResource):
    #method_decorators = [csrf.csrf_check, form_authorization, login_required]
    single_schema = form_schema
    model = FormSubmission
    session = db.session

class FormSubmissionListResource(QueryEngineMixin, BaseResource):
    #method_decorators = [csrf.csrf_check, form_authorization, login_required]
    single_schema = form_schema
    many_schema = forms_schema
    model = FormSubmission
    session = db.session

def get_ip():
    if 'X-Forwarded-For' in request.headers:
        return request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1]
    return request.remote_addr

def google_recaptcha(data):
    return requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data=data)

class SubmissionResource(Resource):
    def post(self, form_name):
        data = request.json

        ## TODO: enforce max_submissions_per_minute

        if data == None or 'recaptcha' not in data:
            abort(400, errors=['Missing recaptcha field'])

        ip = get_ip()

        google_request_data = {
            'secret': GOOGLE_RECAPTCHA_SECRET,
            'response': data['recaptcha'],
            'remoteip': ip
        }

        google_response = google_recaptcha(google_request_data)

        if google_response.status_code != 200:
            ## TODO: log issue with Google
            abort(500)

        google_response_data = google_response.json()

        if google_response_data['success'] != True:
            abort(400, errors=['Failed recaptcha'])

        ## TODO: make sure google_response_data['challenge_ts'] is not to far off
        ## TODO: verify google_response_data['hostname'] against list on form
        ## TODO: inspect google_response_data['error-codes'] ?

        form = db.session.query(Form).filter(Form.name == form_name).one_or_none()

        if form == None:
            abort(404, errors=['Form {} not found'.format(form_name)])

        if form.action == 'store_only':
            status = 'processed'
        else:
            status = 'submitted'

        user_agent = request.user_agent.string
        referrer = request.referrer

        del data['recaptcha']

        submission = FormSubmission(
            form_name=form_name,
            ip=ip,
            user_agent=user_agent,
            referrer=referrer,
            data=data,
            status=status)
        db.session.add(submission)
        db.session.commit()

        return None, 204
