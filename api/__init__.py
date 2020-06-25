import os
from flask import Flask, jsonify, abort, make_response, request, url_for, abort

from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth

from .models import db
from .errors import InvalidUsage
from .auth import auth

from api.v1 import api_v1_bp, API_VERSION_V1

def create_app(config_module=None):
    app = Flask(__name__, static_url_path="")
    app.config.from_object(config_module or
                           os.environ.get('FLASK_CONFIG') or
                           'config')

    db.init_app(app)
    migrate = Migrate(app, db)


    app.register_blueprint(
        api_v1_bp,
        url_prefix=f"{app.config['URL_PREFIX']}/v{API_VERSION_V1}"
    )    

    # @auth.login_required
    @app.route('/')
    def index():
        from api.v1 import get_catelog as v1_catelog
        return {'versions': {"v1": v1_catelog()}}

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not Found'}), 404)

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @auth.get_password
    def get_password(username):
        if username == 'robin':
            return 'python'
        return None

    @auth.error_handler
    def unauthorized():
        return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    return app