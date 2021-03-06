from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from api.utils import get_utc_now

db = SQLAlchemy()

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text, index=True, nullable=True)
    last_done = db.Column(db.DateTime, index=True, default=get_utc_now)
    frequency = db.Column(db.String(64), index=True, default="monthly")
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    def __repr__(self):
        return f"<Job> {self.title}"

    def import_data(self, data):
        try:
            self.title = data['title']
        except KeyError as e:
            raise ValueError('Invalid class: missing ' + e.args[0])
        
        self.description = data.get('description')
        self.frequency = data.get('frequency')
        last_done = data.get('last_done')
        if last_done:
            self.last_done = datetime.strptime(last_done, "%Y-%m-%dT%H:%M:%S.%f")
        else:
            self.last_done = get_utc_now()
        return self

    def export_data(self):
        return {
            'title': self.title,
            'description': self.description,
            'frequency': self.frequency,
            'last_done': self.last_done
        }



# class Location(db.Model): # Like User
#     __tablename__ = 'locations'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), index=True, unique=True)
#     jobs = db.relationship('Job', backref='location', lazy=True)

#     def __repr__(self):
#         return f"<Location> '{self.name}' has jobs: {[job.title for job in self.jobs]}"


# class User(db.Model): # Like User
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#     jobs = db.relationship('Job', backref='worker', lazy='dynamic')
#     def __repr__(self):
#         return f"<User> {self.username} {self.email}"