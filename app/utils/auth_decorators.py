from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import Usuario

def role_required(allowed_roles):
    """
    Decorador para verificar roles específicos
    allowed_roles puede ser string o lista de strings
    """
    def decorator(func):
        @wraps(func)
        @jwt_required()  # Primero verificar que tenga token válido
        def wrapper(*args, **kwargs):
            try:
                claims = get_jwt()
                user_role = claims.get('rol')
                
                # Convertir a lista si es string
                if isinstance(allowed_roles, str):
                    roles = [allowed_roles]
                else:
                    roles = allowed_roles
                
                if user_role not in roles:
                    return jsonify({
                        'success': False,
                        'message': f'Acceso denegado. Requiere rol: {", ".join(roles)}. Tu rol: {user_role}'
                    }), 403
                
                return func(*args, **kwargs)
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Error de autorización: {str(e)}'
                }), 500
        
        return wrapper
    return decorator

def owner_or_admin_required(get_resource_owner_id):
    """
    Decorador para verificar que el usuario sea dueño del recurso o administrador
    get_resource_owner_id: función que retorna el ID del dueño del recurso
    """
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            try:
                current_user_email = get_jwt_identity()
                claims = get_jwt()
                current_user_id = claims.get('user_id')
                current_user_role = claims.get('rol')
                
                # Coordinadores tienen acceso a todo
                if current_user_role == 'coordinador':
                    return func(*args, **kwargs)
                
                # Obtener ID del dueño del recurso
                resource_owner_id = get_resource_owner_id(*args, **kwargs)
                
                if current_user_id != resource_owner_id:
                    return jsonify({
                        'success': False,
                        'message': 'Acceso denegado. Solo puedes acceder a tus propios recursos'
                    }), 403
                
                return func(*args, **kwargs)
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'message': f'Error de autorización: {str(e)}'
                }), 500
        
        return wrapper
    return decorator

def active_user_required(func):
    """Decorador para verificar que el usuario esté activo"""
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        try:
            current_user_email = get_jwt_identity()
            
            usuario = Usuario.query.filter_by(email=current_user_email).first()
            
            if not usuario or not usuario.activo:
                return jsonify({
                    'success': False,
                    'message': 'Cuenta desactivada. Contacte al administrador'
                }), 401
            
            return func(*args, **kwargs)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error de verificación de usuario: {str(e)}'
            }), 500
    
    return wrapper