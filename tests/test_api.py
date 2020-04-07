import os
import tempfile

import pytest
import jobsapi

@pytest.fixture
def client():
    db_fd, jobsapi.app.config['SQLALCHEMY_DATABASE_URI'] = tempfile.mkstemp()
    jobsapi.app.config['TESTING'] = True

    with jobsapi.app.test_client() as client:
        with jobsapi.app.app_context():
            jobsapi.init_db()
        yield client

    os.close(db_fd)
    os.unlink(jobsapi.app.config['SQLALCHEMY_DATABASE_URI'])


def test_something(client):
    print(f"Here is your client: {client}")