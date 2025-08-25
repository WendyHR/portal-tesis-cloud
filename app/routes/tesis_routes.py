from flask import Blueprint, request, jsonify
from app import db
from app.models import Tesis, Usuario
from datetime import datetime

tesis_bp = Blueprint('tesis', __name__)
# Endpoint de salud
@tesis_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'success': True,
        'message': 'API funcionando correctamente',
        'timestamp': datetime.utcnow().isoformat()
    }), 200
    # GET /api/tesis - Listar todas las tesis
@tesis_bp.route('/tesis', methods=['GET'])
def get_all_tesis():
    try:
        tesis = Tesis.query.all()
        return jsonify({
            'success': True,
            'data': [t.to_dict() for t in tesis],
            'total': len(tesis)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al obtener tesis: {str(e)}'
        }), 500

# GET /api/tesis/<id> - Obtener una tesis específica
@tesis_bp.route('/tesis/<int:tesis_id>', methods=['GET'])
def get_tesis(tesis_id):
    try:
        tesis = Tesis.query.get_or_404(tesis_id)
        return jsonify({
            'success': True,
            'data': tesis.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Tesis no encontrada: {str(e)}'
        }), 404

# POST /api/tesis - Crear nueva tesis
@tesis_bp.route('/tesis', methods=['POST'])
def create_tesis():
    try:
        data = request.get_json()
        
        if not data.get('titulo'):
            return jsonify({
                'success': False,
                'message': 'El título es requerido'
            }), 400
        
        nueva_tesis = Tesis(
            titulo=data['titulo'],
            resumen=data.get('resumen', ''),
            estado=data.get('estado', 'borrador'),
            usuario_id=data.get('usuario_id', 1)
        )
        
        db.session.add(nueva_tesis)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tesis creada exitosamente',
            'data': nueva_tesis.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al crear tesis: {str(e)}'
        }), 500
        # PUT /api/tesis/<id> - Actualizar tesis
@tesis_bp.route('/tesis/<int:tesis_id>', methods=['PUT'])
def update_tesis(tesis_id):
    try:
        tesis = Tesis.query.get_or_404(tesis_id)
        data = request.get_json()
        
        if 'titulo' in data:
            tesis.titulo = data['titulo']
        if 'resumen' in data:
            tesis.resumen = data['resumen']
        if 'estado' in data:
            tesis.estado = data['estado']
        
        tesis.fecha_actualizacion = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tesis actualizada exitosamente',
            'data': tesis.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al actualizar tesis: {str(e)}'
        }), 500

# DELETE /api/tesis/<id> - Eliminar tesis
@tesis_bp.route('/tesis/<int:tesis_id>', methods=['DELETE'])
def delete_tesis(tesis_id):
    try:
        tesis = Tesis.query.get_or_404(tesis_id)
        
        db.session.delete(tesis)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tesis eliminada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al eliminar tesis: {str(e)}'
        }), 500