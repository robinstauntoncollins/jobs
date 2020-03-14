from app import db
from datetime import datetime

class Job(db.Model): # Like Post
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text, index=True, nullable=True)
    last_done = db.Column(db.DateTime, index=True, default=datetime.now())
    frequency = db.Column(db.String(64), index=True, default="monthly")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    def __repr__(self):
        return f"<Job> '{self.title}' performed in {self.location.name} assigned to {self.worker.username} performed {self.frequency}"


class Location(db.Model): # Like User
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    jobs = db.relationship('Job', backref='location', lazy=True)

    def __repr__(self):
        return f"<Location> '{self.name}' has jobs: {[job.title for job in self.jobs]}"


class User(db.Model): # Like User
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    jobs = db.relationship('Job', backref='worker', lazy='dynamic')
    def __repr__(self):
        return f"<User> {self.username} {self.email}"