from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig

# Extensiones globales
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Registrar blueprints
    from app.routes.tesis_routes import tesis_bp
    from app.routes.auth_routes import auth_bp  # ← IMPORTANTE: Esta línea
    
    app.register_blueprint(tesis_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')  # ← IMPORTANTE: Esta línea
    
    print("✅ Blueprints registrados: tesis_bp, auth_bp")  # ← DEBUG
    
    return app