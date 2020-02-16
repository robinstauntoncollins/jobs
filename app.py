from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)

auth = HTTPBasicAuth()

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

@app.route('/jobs/api/v1.0/jobs', methods=['GET'])
@auth.login_required
def get_jobs():
    return jsonify({'jobs': [make_public_job(job) for job in jobs]})


@app.route('/jobs/api/v1.0/jobs/<int:job_id>', methods=['GET'])
@auth.login_required
def get_job(job_id):
    job = [job for job in jobs if job['id'] == job_id]
    if len(job) == 0:
        abort(404)
    return jsonify({'job': make_public_job(job[0])})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': "Bad Request"}), 400)


@app.route('/jobs/api/v1.0/jobs', methods=['POSt'])
@auth.login_required
def create_job():
    if not request.json or not 'title' in request.json or not 'location' in request.json or not 'frequency' in request.json:
        abort(400)
    job = {
        'id': jobs[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'location': request.json['location'],
        'frequency': request.json['frequency'],
        'preferred': request.json.get('preferred', ""),
        'done': False
    }
    jobs.append(job)
    return jsonify({'job': make_public_job(job)}), 201


@app.route('/jobs/api/v1.0/jobs/<int:job_id>', methods=['PUT'])
@auth.login_required
def update_job(job_id):
    job = [job for job in jobs if job['id'] == job_id]
    if len(job) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != unicode:
        abort(400)
    if 'location' in request.json and type(request.json['location']) != unicode:
        abort(400)
    if 'frequency' in request.json and type(request.json['frequency']) != unicode:
        abort(400)
    if 'preferred' in request.json and type(request.json['preferred']) != unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) != bool:
        abort(400)
    job[0]['title'] = request.json.get('title', job[0]['title'])
    job[0]['description'] = request.json.get('description', job[0]['description'])
    job[0]['location'] = request.json.get('location', job[0]['location'])
    job[0]['frequency'] = request.json.get('frequency', job[0]['frequency'])
    job[0]['preferred'] = request.json.get('preferred', job[0]['preferred'])
    job[0]['done'] = request.json.get('done', job[0]['done'])
    return jsonify({'job': make_public_job(job[0])})


@app.route('/jobs/api/v1.0/jobs/<int:job_id>', methods=['DELETE'])
@auth.login_required
def delete_job(job_id):
    job = [job for job in jobs if job['id'] == job_id]
    if len(job) == 0:
        abort(404)
    jobs.remove(job[0])
    return jsonify({'result': True})


def make_public_job(job):
    new_job = {}
    for field in job:
        if field == 'id':
            new_job['uri'] = url_for('get_job', job_id=job['id'], _external=True)
        else:
            new_job[field] = job[field]
    return new_job


@auth.get_password
def get_password(username):
    if username == 'robin':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


if __name__ == '__main__':
    app.run(debug=True)