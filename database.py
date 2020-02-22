from app import db


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True),
    description = db.Column(db.Text, index=True, nullable=True)
    location = db.Column(db.String(64), index=True)
    done = db.Column(db.Boolean, index=True, default=False)
    frequency = db.Column(db.String(64), index=True)
    preferred = db.Column(db.String(64), index=True, nullable=True)

    def __repr__(self):
        return f"<Job> {self.title}"