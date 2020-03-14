from datetime import datetime

from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse, fields, marshal

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

app = Flask(__name__, static_url_path="")
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Job': models.Job, 'Location': models.Location, 'User': models.User}

api = Api(app)

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'robin':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


job_fields = {
    'title': fields.String,
    'description': fields.String,
    'last_done': fields.DateTime(dt_format='iso8601'),
    'frequency': fields.String,
    'worker': fields.String,
    'location': fields.String,
    'uri': fields.Url('job'),
}

class JobListAPI(Resource):

    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help="No job title provided", location="json")
        self.reqparse.add_argument('description', type=str, default="", location="json")
        self.reqparse.add_argument('location', type=str, required=True, location="json", help="No location provided")
        self.reqparse.add_argument('frequency', type=str, default="weekly", location="json")
        self.reqparse.add_argument('worker', type=str, default="", location="json")
        super(JobListAPI, self).__init__()

    def get(self):
        jobs = models.Job.query.all()
        return {'jobs': [marshal(job, job_fields) for job in jobs]}

    def post(self):
        args = self.reqparse.parse_args()
        jobs = models.Job.query.all()
        if not args.get('last_done'):
            last_done = datetime.now()
        else:
            last_done = args['last_done']
        j = models.Job(
            title=args['title'],
            description=args['description'],
            location=models.Location.query.filter_by(name=args['location']).first(),
            frequency=args['frequency'],
            worker=models.User.query.filter_by(username=args['worker']).first(),
            last_done=last_done
        )
        db.session.add(j)
        db.session.commit()
        return {'job': marshal(j, job_fields)}, 201

class JobAPI(Resource):

    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location="json")
        self.reqparse.add_argument('description', type=str, default="", location="json")
        self.reqparse.add_argument('location', type=str, location="json")
        self.reqparse.add_argument('frequency', type=str, default="weekly", location="json")
        self.reqparse.add_argument('worker', type=str, default="", location="json")
        self.reqparse.add_argument('last_done', type=bool, default=datetime.now().isoformat(), location="json")
        super(JobAPI, self).__init__()

    def get(self, id):
        job = models.Job.query.get_or_404(id)
        return {'job': marshal(job, job_fields)},

    def put(self, id):
        job = models.Job.query.get_or_404(id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                pass
        return {'job': marshal(job, job_fields)}

    def delete(self, id):
        job = models.Job.query.get_or_404(id)
        db.session.delete(job)
        db.session.commit()
        return {'result': True}

api.add_resource(JobListAPI, '/jobs/api/v1.0/jobs', endpoint='jobs')
api.add_resource(JobAPI, '/jobs/api/v1.0/jobs/<int:id>', endpoint='job')


if __name__ == '__main__':
    app.run(debug=True)