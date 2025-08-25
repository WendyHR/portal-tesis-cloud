from app import create_app, db
from app.models import Usuario, Tesis, Avance, Comentario
from faker import Faker
import os

app = create_app()
fake = Faker('es_ES')

def create_sample_data():
    # ... tu función existente ...
    pass

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
        
        # DEBUG: Mostrar todas las rutas registradas
        print("\n📋 RUTAS REGISTRADAS:")
        for rule in app.url_map.iter_rules():
            print(f"   {list(rule.methods)} {rule.rule}")
        print()
    
    print("🚀 Servidor iniciando en http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)