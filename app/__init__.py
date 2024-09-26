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

    # Load configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Ensure this is correctly set
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DEBUG'] = True if os.getenv('APP_ENV') == 'development' else False

    print("DATABASE_URL:", app.config['SQLALCHEMY_DATABASE_URI'])  # Check what is being loaded

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes  # Import routes here to register them

    return app
