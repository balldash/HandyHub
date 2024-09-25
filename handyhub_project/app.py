from flask import Flask
from flask_jwt_extended import JWTManager
from api.models import db
from config import Config
from api.routes.tradesman import tradesmen_bp
from api.routes.clients import clients_bp
from api.routes.jobs import jobs_bp
from api.routes.quotations import quotations_bp

app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = Config.SECRET_KEY

jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(tradesmen_bp, url_prefix='/api')
app.register_blueprint(clients_bp, url_prefix='/api')
app.register_blueprint(jobs_bp, url_prefix='/api')
app.register_blueprint(quotations_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
