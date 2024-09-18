from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


# Database configuration
app.config['SQLAlCHEMY_DATABASE_URI'] = 'mysql://bislon'

# API route to check the status of the application

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'ok',
        'message': 'HandyHub API is running',
        'version': '1.0.0'
        }), 200

if __name__ == '__main__':
    app.run(debug=True)
