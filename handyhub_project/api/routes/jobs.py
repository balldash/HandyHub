from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import Job, Review, db

jobs_bp = Blueprint('jobs', __name__)


@jobs_bp.route('/jobs/available', methods=['GET'])
@jwt_required()
def get_available_jobs():
    status = request.args.get('status', 'available')
    specialization = request.args.get('specialization', None)

    query = Job.query.filter_by(status=status)

    if specialization:
        query = query.filter_by(specialization=specialization)

    jobs = query.all()
    return jsonify([job.to_dict() for job in jobs])


@jobs_bp.route('/jobs/past', methods=['GET'])
@jwt_required()
def get_past_jobs():
    user_id = get_jwt_identity()['id']
    jobs = Job.query.filter((Job.user_id == user_id)
                            | (Job.tradesman_id == user_id)
                            ).filter(Job.status != 'available').all()
    return jsonify([job.to_dict() for job in jobs])


@jobs_bp.route('/jobs/<int:job_id>/reviews', methods=['GET'])
@jwt_required()
def get_job_reviews(job_id):
    reviews = Review.query.filter_by(job_id=job_id).all()
    return jsonify([review.to_dict() for review in reviews])


@jobs_bp.route('/jobs', methods=['POST'])
@jwt_required()
def create_job():
    data = request.get_json()
    new_job = Job(
        title=data['title'],
        description=data['description'],
        location=data['location'],
        address=data['address'],
        specialization=data['specialization'],
        user_id=get_jwt_identity()['id'],
        status='available'
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify(new_job.to_dict()), 201