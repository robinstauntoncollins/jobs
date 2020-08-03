from api import create_app, db, models
from config import Config

import click


app = create_app(Config)
    
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Job': models.Job}


@app.cli.command('createdb')
@click.option('--test-data', type=bool, default=True, help="Initializes database with pre-loaded data")
def createdb(test_data):
    db.drop_all()
    db.create_all()
    if test_data:
        job_data = [
            {'title': "Wash the Dishes"},
            {'title': 'Vacuum Bedroom'},
            {'title': 'Dust surfaces in Bedroom'}
        ]

        jobs = [models.Job().import_data(j) for j in job_data]
        db.session.add_all(jobs)

        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)