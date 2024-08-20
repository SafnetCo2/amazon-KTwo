import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    # Print the DATABASE_URL to check if it's set
    print("DATABASE_URL:", os.getenv('DATABASE_URL'))

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes  # Import routes here to register them

    return app
