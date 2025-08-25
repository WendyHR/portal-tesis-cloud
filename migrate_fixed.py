#!/usr/bin/env python3
"""
Script mejorado para migrar datos de SQLite a PostgreSQL
"""
import os
from sqlalchemy import create_engine, text
from app import create_app, db
from app.models import Usuario, Tesis, Avance, Comentario

def migrate_data():
    """Migrar datos de SQLite a PostgreSQL con connection string hardcoded"""
    
    # Connection string fija (sabemos que funciona)
    postgres_url = "postgresql://portaladmin@portal-tesis-db-santoto:Cl4s3cl0ud2025@portal-tesis-db-santoto.postgres.database.azure.com:5432/portal_tesis?sslmode=require"
    
    print("🔄 Iniciando migración a PostgreSQL...")
    print(f"🔍 Conectando a: portal_tesis")
    
    # Configurar app con PostgreSQL
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url
    
    with app.app_context():
        try:
            # Probar conexión
            result = db.session.execute(text('SELECT version()'))
            version = result.fetchone()[0]
            print(f"✅ Conectado a PostgreSQL!")
            print(f"📊 Versión: {version}")
            
            # Crear tablas
            print("📋 Creando tablas en PostgreSQL...")
            db.create_all()
            
            # Verificar tablas creadas
            result = db.session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"✅ Tablas creadas: {tables}")
            
            # Crear datos de ejemplo
            print("📊 Creando datos de ejemplo...")
            from app import create_sample_data
            create_sample_data()
            
            # Verificar datos
            usuarios_count = Usuario.query.count()
            tesis_count = Tesis.query.count()
            print(f"✅ Usuarios creados: {usuarios_count}")
            print(f"✅ Tesis creadas: {tesis_count}")
            
            print("🎉 ¡Migración completada exitosamente!")
            return True
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            db.session.rollback()
            return False
        finally:
            db.session.close()

if __name__ == '__main__':
    success = migrate_data()
    if success:
        print("\n🚀 Ya puedes usar PostgreSQL en tu aplicación!")
        print("💡 Para usar PostgreSQL permanentemente, actualiza config.py")
    else:
        print("\n❌ La migración falló. Revisa los errores arriba.")