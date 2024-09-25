from datetime import datetime
from . import db


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    tradesman_id = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'address': self.address,
            'specialization': self.specialization,
            'user_id': self.user_id,
            'tradesman_id': self.tradesman_id,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
