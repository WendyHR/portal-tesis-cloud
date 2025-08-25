import os
from datetime import timedelta

class Config:
    # Database - Configuración universal
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///portal_tesis.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string-super-secure'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # CORS - Permitir Azure Static Web Apps
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "https://*.azurestaticapps.net"  # Permitir cualquier Azure Static Web App
    ]

class DevelopmentConfig(Config):
    DEBUG = True
     # Cambiar SQLite por PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://portaladmin:Cl4s3cl0ud2025@portal-tesis-db-santoto.postgres.database.azure.com:5432/portal_tesis?sslmode=require'

class ProductionConfig(Config):
    DEBUG = False
    # En producción, estas variables DEBEN venir del entorno
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    
    # PostgreSQL en Azure
    if not os.environ.get('DATABASE_URL'):
        # Fallback si no está configurada la variable
        SQLALCHEMY_DATABASE_URI = 'sqlite:///portal_tesis.db'