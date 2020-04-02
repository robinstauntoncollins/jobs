from flask import Blueprint, g # url_for
from flask_restful import Api


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


# def get_catelog():
#     return {
#         'jobs_url': Api.url_for(, _external=True)
#     }

from . import jobs
