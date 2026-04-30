from flask import Flask
from .routers.questions import questions_bp
from .routers.response import response_bp
from config import DevelopmentConfig
from .models import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db, directory='app/migrations')
    app.register_blueprint(questions_bp)
    app.register_blueprint(response_bp)
    return app