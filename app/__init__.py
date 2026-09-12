from flask import Flask
from flask_cors import CORS
from app.models import db
import os

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'data', 'taxsee.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'rahasia_super_kuat_123')
    
    db.init_app(app)
    
    from app.routes.auth import auth_bp
    from app.routes.shifts import shifts_bp
    from app.routes.balance import balance_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(shifts_bp)
    app.register_blueprint(balance_bp)
    app.register_blueprint(admin_bp)
    
    with app.app_context():
        db.create_all()
    
    return app
