import os
from pathlib import Path

basedir = Path.cwd()

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + str(basedir) + 'app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False