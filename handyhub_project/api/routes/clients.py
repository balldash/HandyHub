from flask import Blueprint, request, jsonify
from flask_jwt_extended import (create_access_token,
                                get_jwt_identity,
                                jwt_required)
from ..models import Client, db

clients_bp = Blueprint('clients', __name__)


# GET: Retrieve all clients
@clients_bp.route('/clients', methods=['GET'])
@jwt_required()
def get_clients():
    try:
        clients = Client.query.all()

        if not clients:
            return jsonify({
                "message": "No clients found.",
                "data": []
            }), 200

        return jsonify({
            "message": "List of all clients retrieved successfully.",
            "data": [c.to_dict() for c in clients]
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"An error occurred while fetching clients: {str(e)}"
        }), 500


# GET: Retrieve a single client by id
@clients_bp.route('/clients/<int:id>', methods=['GET'])
@jwt_required()
def get_client(id):
    try:
        client = Client.query.get_or_404(id)

        return jsonify({
            "message": "Client found.",
            "data": client.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"An error occurred while retrieving the client: {str(e)}"
        }), 500


# POST: Create a new client
@clients_bp.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()

    # Validate input fields
    required_fields = ('name', 'email', 'phone', 'location', 'password')
    if not data or not all(field in data for field in required_fields):
        return jsonify({
            "error": "Invalid request. Please provide all required fields."
        }), 400

    # Create a new client instance
    new_client = Client(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        location=data['location'],
        password=data['password']
    )

    try:
        db.session.add(new_client)
        db.session.commit()
        return jsonify({
            "message": "Client successfully registered.",
            "data": new_client.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An error occurred while registering: {str(e)}"
        }), 500


# PUT: Update client information by id
@clients_bp.route('/clients/<int:id>', methods=['PUT'])
@jwt_required()
def update_client(id):
    client = Client.query.get_or_404(id)
    data = request.get_json()

    # Update client fields
    client.name = data.get('name', client.name)
    client.email = data.get('email', client.email)
    client.phone = data.get('phone', client.phone)
    client.location = data.get('location', client.location)
    client.password = data.get('password', client.password)

    try:
        db.session.commit()
        return jsonify({
            "message": "Client successfully updated.",
            "data": client.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An error occurred while updating: {str(e)}"
        }), 500


# DELETE: Remove a client by id
@clients_bp.route('/clients/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_client(id):
    client = Client.query.get_or_404(id)

    try:
        db.session.delete(client)
        db.session.commit()
        return jsonify({
            "message": f"Client with id {id} successfully deleted."
        }), 204

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"An error occurred while deleting: {str(e)}"
        }), 500


# POST: Login for clients, generate JWT
@clients_bp.route('/clients/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = Client.query.filter_by(email=email).first()

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
@clients_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({
        "message": "Access granted.",
        "logged_in_as": current_user
    }), 200
