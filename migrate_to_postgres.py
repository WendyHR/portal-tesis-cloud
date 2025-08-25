#!/usr/bin/env python3
"""
Script para migrar datos de SQLite a PostgreSQL
"""
import os
import sys
from sqlalchemy import create_engine, text
from app import create_app, db
from app.models import Usuario, Tesis, Avance, Comentario

def migrate_data(postgres_url):
    """Migrar datos de SQLite a PostgreSQL"""
    
    print("🔄 Iniciando migración a PostgreSQL...")
    
    # LIMPIAR la URL completamente
    postgres_url = postgres_url.strip()  # Quitar espacios
    
    # Si contiene texto después de "require", cortarlo
    if "?sslmode=require" in postgres_url:
        postgres_url = postgres_url.split("?sslmode=require")[0] + "?sslmode=require"
    
    print(f"🔍 URI limpia: '{postgres_url}'")
    
    # Configurar app con PostgreSQL
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url
    
    with app.app_context():
        try:
            # Probar conexión
            result = db.session.execute(text('SELECT version()'))
            version = result.fetchone()[0]
            print(f"✅ Conectado a PostgreSQL: {version}")
            
            # Crear tablas
            print("📋 Creando tablas...")
            db.create_all()
            
            # Crear datos de ejemplo
            print("📊 Creando datos de ejemplo...")
            from app import create_sample_data
            create_sample_data()
            
            print("✅ Migración completada exitosamente!")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            db.session.rollback()
        finally:
            db.session.close()

if __name__ == '__main__':
    print("📋 Ingresa la connection string de PostgreSQL:")
    print("Ejemplo: postgresql://usuario:password@servidor:5432/database?sslmode=require")
    postgres_url = input("Connection string: ")
    migrate_data(postgres_url)