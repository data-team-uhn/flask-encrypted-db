from flask import Flask
from config import config
from flask_cors import CORS
from flask_migrate import Migrate
from utils import CustomJsonEncoder

# Import database models with app context
from models import db

migrate = Migrate()
cors = CORS(methods=['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE'])


def forbidden_method(e):
    return {"error": "You're not authorized to access this method"}, 405


def endpoint_not_found(e):
    return {"error": "This endpoint does not exist"}, 404


def create_app():
    app = Flask(__name__)

    app.json_encoder = CustomJsonEncoder
    app.config.from_object(config)

    app.register_error_handler(405, forbidden_method)
    app.register_error_handler(404, endpoint_not_found)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Register blueprints
    from endpoints import users
    app.register_blueprint(users.bp)

    # Function for removing sessions after context is no longer needed
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    app.use_reloader = False
    return app
