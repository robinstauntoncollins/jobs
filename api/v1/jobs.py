from datetime import datetime
from flask_restful import Resource, reqparse, fields, marshal
from api.auth import auth
from . import api
from api import models

job_fields = {
    'title': fields.String,
    'description': fields.String,
    'last_done': fields.DateTime(dt_format='iso8601'),
    'frequency': fields.String,
    'uri': fields.Url('api.job'),
}

class JobListAPI(Resource):

    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help="No job title provided", location="json")
        self.reqparse.add_argument('description', type=str, default="", location="json")
        self.reqparse.add_argument('last_done', type=str, default=datetime.utcnow, location="json")
        self.reqparse.add_argument('frequency', type=str, default="weekly", location="json")
        super(JobListAPI, self).__init__()

    def get(self):
        jobs = models.Job.query.all()
        return {'jobs': [marshal(job, job_fields) for job in jobs]}

    def post(self):
        args = self.reqparse.parse_args()
        job = models.Job.query.filter_by(title=args['title']).first()
        if job is not None:
            raise InvalidUsage(f"Job with this title already exists")
        job = models.Job().import_data(args)
        models.db.session.add(job)
        models.db.session.commit()
        return {'job': marshal(job, job_fields)}, 201

class JobAPI(Resource):

    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location="json")
        self.reqparse.add_argument('description', type=str, location="json")
        self.reqparse.add_argument('frequency', type=str, location="json")
        self.reqparse.add_argument('last_done', type=str, location="json")
        super(JobAPI, self).__init__()

    def get(self, id):
        job = models.Job.query.get_or_404(id)
        return {'job': marshal(job, job_fields)},

    def put(self, id):
        job = models.Job.query.get_or_404(id)
        job_current_data = job.export_data()
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is None:
                args[k] = job_current_data[k]
        job.import_data(args)
        models.db.session.add(job)
        models.db.session.commit()
        return {'job': marshal(job, job_fields)}

    def delete(self, id):
        job = models.Job.query.get_or_404(id)
        models.db.session.delete(job)
        models.db.session.commit()
        return {'result': True}
