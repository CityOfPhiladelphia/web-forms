import os

import flask
from flask_restful import Api
from flask_cors import CORS

from web_forms.models import db
from web_forms import resources

app = flask.Flask(__name__)
app.config['DEBUG'] = os.getenv('DEBUG', False)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

db.init_app(app)
api = Api(app)
CORS(app, supports_credentials=True)

with app.app_context():
    api.add_resource(resources.FormListResource, '/forms')
    api.add_resource(resources.FormResource, '/forms/<instance_id>')

    api.add_resource(resources.FormSubmissionListResource, '/submissions')
    api.add_resource(resources.FormSubmissionResource, '/submissions/<int:instance_id>')

    api.add_resource(resources.SubmissionResource, '/forms/<form_name>/submissions')

## dev server
if __name__ == '__main__':
    app.run(host='0.0.0.0')
