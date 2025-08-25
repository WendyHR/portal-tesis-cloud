from app import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='estudiante')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    tesis = db.relationship('Tesis', backref='autor', lazy=True)
    comentarios = db.relationship('Comentario', backref='autor', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nombre': self.nombre,
            'rol': self.rol,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

class Tesis(db.Model):
    __tablename__ = 'tesis'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    resumen = db.Column(db.Text)
    estado = db.Column(db.String(20), default='borrador')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Relaciones
    avances = db.relationship('Avance', backref='tesis', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'resumen': self.resumen,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'usuario_id': self.usuario_id,
            'autor_nombre': self.autor.nombre if self.autor else None
        }

class Avance(db.Model):
    __tablename__ = 'avances'
    
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.Text, nullable=False)
    archivo_url = db.Column(db.String(255))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    tesis_id = db.Column(db.Integer, db.ForeignKey('tesis.id'), nullable=False)
    
    # Relaciones
    comentarios = db.relationship('Comentario', backref='avance', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'archivo_url': self.archivo_url,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'tesis_id': self.tesis_id
        }

class Comentario(db.Model):
    __tablename__ = 'comentarios'
    
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    avance_id = db.Column(db.Integer, db.ForeignKey('avances.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'texto': self.texto,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'usuario_id': self.usuario_id,
            'avance_id': self.avance_id,
            'autor_nombre': self.autor.nombre if self.autor else None
        }