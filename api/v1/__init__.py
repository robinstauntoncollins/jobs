from flask import Blueprint, g 
from flask_restful import Api



API_VERSION_V1 = 1

api_v1_bp = Blueprint('api', __name__)
api = Api(api_v1_bp)


from . import jobs
api.add_resource(jobs.JobListAPI, '/jobs', '/jobs/', endpoint='jobs')
api.add_resource(jobs.JobAPI, '/jobs/<int:id>', '/jobs/<int:id>/', endpoint='job')


def get_catelog():
    return {
        'jobs_url': api.url_for(jobs.JobListAPI, _external=True)
    }