from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource, reqparse, fields, marshal

app = Flask(__name__, static_url_path="")
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



jobs = [
    {
        'id': 1,
        'title': 'Clean Bathroom Mirror',
        'description': 'Use glass cleaner to clean the bathroom mirror.',
        'location': 'bathroom',
        'done': False,
        'frequency': 'weekly',
        'preferred': 'Robin',
    },
    {
        'id': 2,
        'title': 'Wash kitchen floor',
        'description': 'Mop kitchen and dining room floor as far as the fridge',
        'location': 'kitchen',
        'done': False,
        'frequency': 'monthly',
        'preferred': 'Karolina',        
    }
]

job_fields = {
    'title': fields.String,
    'location': fields.String,
    'frequency': fields.String,
    'preferred': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('job')
}

class JobListAPI(Resource):

    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help="No job title provided", location="json")
        self.reqparse.add_argument('description', type=str, default="", location="json")
        self.reqparse.add_argument('location', type=str, required=True, location="json", help="No location provided")
        self.reqparse.add_argument('frequency', type=str, default="weekly", location="json")
        self.reqparse.add_argument('preferred', type=str, default="", location="json")
        super(JobListAPI, self).__init__()

    def get(self):
        return {'jobs': [marshal(job, job_fields) for job in jobs]}

    def post(self):
        args = self.reqparse.parse_args()
        job = {
            'id': jobs[-1]['id'] + 1 if len(jobs) > 0 else 1,
            'title': args['title'],
            'description': args['description'],
            'location': args['location'],
            'frequency': args['frequency'],
            'preferred': args['preferred'],
            'done': False
        }
        jobs.append(job)
        return {'job': marshal(job, job_fields)}, 201

class JobAPI(Resource):

    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location="json")
        self.reqparse.add_argument('description', type=str, default="", location="json")
        self.reqparse.add_argument('location', type=str, location="json")
        self.reqparse.add_argument('frequency', type=str, default="weekly", location="json")
        self.reqparse.add_argument('preferred', type=str, default="", location="json")
        self.reqparse.add_argument('done', type=bool, default=False, location="json")
        super(JobAPI, self).__init__()

    def get(self, id):
        job = [job for job in jobs if job['id'] == id]
        if len(job) == 0:
            abort(404)
        return {'job': marshal(job[0], job_fields)}

    def put(self, id):
        job = [job for job in jobs if job['id'] == id]
        if len(job) == 0:
            abort(404)
        job = job[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                job[k] = v
        return {'job': marshal(job, job_fields)}

    def delete(self, id):
        job = [job for job in jobs if job['id'] == id]
        if len(job) == 0:
            abort(404)
        jobs.remove(job[0])
        return {'result': True}

api.add_resource(JobListAPI, '/jobs/api/v1.0/jobs', endpoint='jobs')
api.add_resource(JobAPI, '/jobs/api/v1.0/jobs/<int:id>', endpoint='job')


if __name__ == '__main__':
    app.run(debug=True)