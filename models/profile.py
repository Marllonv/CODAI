from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey
from extensions import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telefone = db.Column(db.String(11), nullable=True)
    bio = db.Column(db.String(100), nullable=True)
    foto = db.Column(db.String(200), nullable=True)
    foto_thumb = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    user = db.relationship(
        'User',
        back_populates='perfil', 
        uselist=False
    )

    # Remove duplicata de user_id
    # Adiciona métodos utilitários
    def update_from_form(self, form):
        self.telefone = form.get('telefone')
        self.bio = form.get('bio')
        self.foto = form.get('foto')
        self.foto_thumb = form.get('foto_thumb')

    def to_dict(self):
        return {
            'id': self.id,
            'telefone': self.telefone,
            'bio': self.bio,
            'foto': self.foto,
            'foto_thumb': self.foto_thumb,
            'user_id': self.user_id
        }