from flask import Flask, request, jsonify, abort
from models import db, Tradesman, Client
from config import Config


app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)


# Create the database tables
with app.app_context():
    db.create_all()


# API route to check the status of the application
@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'ok',
        'message': 'HandyHub API is running',
        'version': '1.0.0'
    })


@app.route('/api/tradesmen', methods=['GET'])
def get_tradesmen():
    tradesmen = Tradesman.query.all()
    return jsonify([t.to_dict() for t in tradesmen])


@app.route('/api/tradesmen/<int:id>', methods=['GET'])
def get_tradesman(id):
    tradesman = Tradesman.query.get_or_404(id)
    return jsonify(tradesman.to_dict())


@app.route('/api/tradesmen', methods=['POST'])
def create_tradesman():
    data = request.get_json()
    if not data or not all(key in data for key in ('name',
                                                   'email', 'location',
                                                   'specialization',
                                                   'password')):
        abort(400, description="Missing fields")
    new_tradesman = Tradesman(
        name=data['name'],
        email=data['email'],
        location=data['location'],
        specialization=data['specialization'],
        password=data['password']
    )
    db.session.add(new_tradesman)
    db.session.commit()
    return jsonify(new_tradesman.to_dict()), 201


@app.route('/api/tradesmen/<int:id>', methods=['PUT'])
def update_tradesman(id):
    tradesman = Tradesman.query.get_or_404(id)
    data = request.get_json()

    tradesman.name = data.get('name', tradesman.name)
    tradesman.email = data.get('email', tradesman.email)
    tradesman.location = data.get('location', tradesman.location)
    tradesman.specialization = data.get('specialization',
                                        tradesman.specialization)
    tradesman.password = data.get('password', tradesman.password)

    db.session.commit()
    return jsonify(tradesman.to_dict())


@app.route('/api/tradesmen/<int:id>', methods=['DELETE'])
def delete_tradesman(id):
    tradesman = Tradesman.query.get_or_404(id)
    db.session.delete(tradesman)
    db.session.commit()
    return '', 204

# Client Routes


@app.route('/api/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([c.to_dict() for c in clients])


@app.route('/api/clients/<int:id>', methods=['GET'])
def get_client(id):
    client = Client.query.get_or_404(id)
    return jsonify(client.to_dict())


@app.route('/api/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    if not data or not all(key in data for key in ('name',
                                                   'email', 'password')):
        abort(400, description="Missing fields")
    new_client = Client(
        name=data['name'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify(new_client.to_dict()), 201


@app.route('/api/clients/<int:id>', methods=['PUT'])
def update_client(id):
    client = Client.query.get_or_404(id)
    data = request.get_json()

    client.name = data.get('name', client.name)
    client.email = data.get('email', client.email)
    client.password = data.get('password', client.password)

    db.session.commit()
    return jsonify(client.to_dict())


@app.route('/api/clients/<int:id>', methods=['DELETE'])
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
