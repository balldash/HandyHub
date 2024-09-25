from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token,
                                get_jwt_identity,
                                jwt_required)
from ..models import Tradesman, db

tradesmen_bp = Blueprint('tradesmen', __name__)


# GET all tradesmen (JWT required)
@tradesmen_bp.route('/tradesmen', methods=['GET'])
@jwt_required()
def get_tradesmen():
    tradesmen = Tradesman.query.all()
    return jsonify({
        "message": "List of all tradesmen",
        "data": [t.to_dict() for t in tradesmen]
    }), 200


# GET a single tradesman by id
@tradesmen_bp.route('/tradesmen/<int:id>', methods=['GET'])
@jwt_required()
def get_tradesman(id):
    tradesman = Tradesman.query.get_or_404(id)
    return jsonify({
        "message": "Tradesman found",
        "data": tradesman.to_dict()
    }), 200


# POST: Create a new tradesman
@tradesmen_bp.route('/tradesmen', methods=['POST'])
@jwt_required()
def create_tradesman():
    data = request.get_json()

    # Validate input fields
    required_fields = ('name', 'email', 'phone', 'location', 'specialization',
                       'password')
    if not data or not all(field in data for field in required_fields):
        return jsonify({
            "error": "Invalid request. Ensure all fields are provided."
        }), 400

    # Create a new tradesman instance
    new_tradesman = Tradesman(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        location=data['location'],
        specialization=data['specialization'],
        password=data['password']
    )

    try:
        db.session.add(new_tradesman)
        db.session.commit()
        return jsonify({
            "message": "Tradesman successfully registered.",
            "data": new_tradesman.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An error occurred while registering: {str(e)}"
        }), 500


# PUT: Update a tradesman by id
@tradesmen_bp.route('/tradesmen/<int:id>', methods=['PUT'])
@jwt_required()
def update_tradesman(id):
    tradesman = Tradesman.query.get_or_404(id)
    data = request.get_json()

    # Update tradesman fields, use existing values if not provided
    tradesman.name = data.get('name', tradesman.name)
    tradesman.email = data.get('email', tradesman.email)
    tradesman.location = data.get('location', tradesman.location)
    tradesman.specialization = data.get('specialization',
                                        tradesman.specialization)
    tradesman.password = data.get('password', tradesman.password)

    try:
        db.session.commit()
        return jsonify({
            "message": "Tradesman successfully updated.",
            "data": tradesman.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An error occurred while updating: {str(e)}"
        }), 500


# DELETE: Delete a tradesman by id
@tradesmen_bp.route('/tradesmen/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_tradesman(id):
    tradesman = Tradesman.query.get_or_404(id)

    try:
        db.session.delete(tradesman)
        db.session.commit()
        return jsonify({
            "message": f"Tradesman with id {id} successfully deleted."
        }), 204

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An error occurred while deleting: {str(e)}"
        }), 500


# POST: Login a tradesman and generate JWT
@tradesmen_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = Tradesman.query.filter_by(email=email).first()

    if user and user.password == password:
        access_token = create_access_token(identity={'id': user.id,
                                                     'email': user.email})
        return jsonify({
            "message": "Login successful.",
            "access_token": access_token
        }), 200
    else:
        return jsonify({
            "error": "Invalid email or password."
        }), 401


# Protected route (JWT required)
@tradesmen_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({
        "message": "Access granted.",
        "logged_in_as": current_user
    }), 200
