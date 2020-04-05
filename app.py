from api import create_app, db, models
from config import Config


app = create_app(Config)
    
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Job': models.Job}

if __name__ == '__main__':
    app.run(debug=True)