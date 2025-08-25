from flask import Blueprint, request, jsonify
from app import db
from app.models import Usuario

auth_bp = Blueprint('auth', __name__)
# POST /api/auth/register
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No se enviaron datos'
            }), 400
        
        email = data.get('email', '').lower().strip()
        nombre = data.get('nombre', '').strip()
        password = data.get('password', '')
        rol = data.get('rol', 'estudiante')
        
        if not email or not nombre or not password:
            return jsonify({
                'success': False,
                'message': 'Email, nombre y contraseña son requeridos'
            }), 400
        
        existing_user = Usuario.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'El email ya está registrado'
            }), 409
        
        nuevo_usuario = Usuario(
            email=email,
            nombre=nombre,
            password_hash=password,
            rol=rol
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'data': {
                'user': nuevo_usuario.to_dict()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500
        # POST /api/auth/login
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No se enviaron datos'
            }), 400
        
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email y contraseña son requeridos'
            }), 400
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario:
            return jsonify({
                'success': False,
                'message': 'Usuario no encontrado'
            }), 404
        
        if usuario.password_hash != password:
            return jsonify({
                'success': False,
                'message': 'Contraseña incorrecta'
            }), 401
        
        return jsonify({
            'success': True,
            'message': 'Login exitoso',
            'data': {
                'user': usuario.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

# GET /api/auth/users - Listar usuarios
@auth_bp.route('/auth/users', methods=['GET'])
def list_users():
    try:
        usuarios = Usuario.query.all()
        
        return jsonify({
            'success': True,
            'data': [usuario.to_dict() for usuario in usuarios],
            'total': len(usuarios)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500