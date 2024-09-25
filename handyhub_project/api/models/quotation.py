from datetime import datetime
from . import db


class Quotation(db.Model):
    __tablename__ = 'quotations'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, nullable=False)
    tradesman_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now,
                           onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'tradesman_id': self.tradesman_id,
            'amount': self.amount,
            'comment': self.comment,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
