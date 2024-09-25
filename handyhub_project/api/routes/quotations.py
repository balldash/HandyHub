from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import db, Job, Quotation

quotations_bp = Blueprint('quotations', __name__)


# POST: Create a new quotation
@quotations_bp.route('/quotations', methods=['POST'])
@jwt_required()
def create_quotation():
    try:
        data = request.get_json()

        if not data or not all(key in data for key in ('job_id',
                                                       'amount', 'comment')):
            abort(400, description="Missing required fields")

        job_id = data['job_id']
        amount = data['amount']
        comment = data['comment']
        tradesman_id = get_jwt_identity()['id']

        job = Job.query.get_or_404(job_id)

        if job.status != 'available':
            return jsonify({
                "message": "The job is no longer available for quotations.",
                "error": "Job not available"
            }), 400

        new_quotation = Quotation(
            job_id=job_id,
            tradesman_id=tradesman_id,
            amount=amount,
            comment=comment
        )
        db.session.add(new_quotation)
        db.session.commit()

        return jsonify({
            "message": "Quotation created successfully.",
            "data": new_quotation.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            "error": f"An error occurred while creating: {str(e)}"
        }), 500


# PUT: Accept a quotation
@quotations_bp.route('/quotations/<int:quotation_id>/accept', methods=['PUT'])
@jwt_required()
def accept_quotation(quotation_id):
    try:
        quotation = Quotation.query.get_or_404(quotation_id)
        job = Job.query.get_or_404(quotation.job_id)

        if job.user_id != get_jwt_identity()['id']:
            return jsonify({
                "message": "You are not authorized to accept this quotation.",
                "error": "Unauthorized"
            }), 403

        quotation.status = 'accepted'
        job.status = 'in_progress'
        db.session.commit()

        return jsonify({
            "message": "Quotation accepted successfully.",
            "data": quotation.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"An error occurred while accepting: {str(e)}"
        }), 500


# PUT: Reject a quotation
@quotations_bp.route('/quotations/<int:quotation_id>/reject', methods=['PUT'])
@jwt_required()
def reject_quotation(quotation_id):
    try:
        quotation = Quotation.query.get_or_404(quotation_id)
        job = Job.query.get_or_404(quotation.job_id)

        if job.user_id != get_jwt_identity()['id']:
            return jsonify({
                "message": "You are not authorized to reject this quotation.",
                "error": "Unauthorized"
            }), 403

        quotation.status = 'rejected'
        db.session.commit()

        return jsonify({
            "message": "Quotation rejected successfully.",
            "data": quotation.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"An error occurred while rejecting quotation: {str(e)}"
        }), 500
