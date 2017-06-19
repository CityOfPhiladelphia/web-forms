from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB, INET

db = SQLAlchemy()

## TODO: success redirect ?
## TODO: failure redirect ?
## TODO: failure page - for pure HTML forms
## TODO: place constraint on name, like [a-z\-]+
class Form(db.Model):
    __tablename__ = 'forms'

    name = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    schema = db.Column(JSONB)
    action = db.Column(db.Enum('store_only',
                               'google_sheets',
                               'webhook',
                               'taskflow_task',
                               'taskflow_workflow',
                               name='form_actions'),
                       nullable=False)
    action_config = db.Column(JSONB)
    max_submissions_per_minute = db.Column(db.Integer, nullable=False, default=5)
    forms = db.relationship('FormSubmission', backref='form', lazy='dynamic', passive_deletes=True)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now())
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now(),
                           onupdate=func.now())

class FormSubmission(db.Model):
    __tablename__ = 'form_submissions'

    id = db.Column(db.Integer, primary_key=True)
    form_name = db.Column(db.String, db.ForeignKey('forms.name', ondelete='CASCADE'))
    ip = db.Column(INET, nullable=False)
    user_agent = db.Column(db.String)
    referrer = db.Column(db.String)
    data = db.Column(JSONB)
    status = db.Column(db.Enum('submitted',
                               'processing',
                               'retrying',
                               'canceled',
                               'failed',
                               'processed',
                               name='form_submission_statuses'),
                       nullable=False)
    locked_at = db.Column(db.DateTime)
    worker_id = db.Column(db.String)
    attempts = db.Column(db.Integer, nullable=False, default=0)
    max_attempts = db.Column(db.Integer, nullable=False, default=1)
    timeout = db.Column(db.Integer, nullable=False, default=600)
    retry_delay = db.Column(db.Integer, nullable=False, default=300)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now())
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=func.now(),
                           onupdate=func.now())
