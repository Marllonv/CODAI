from extensions import db
from datetime import datetime

class ArticleCategory(db.Model):
    """Categorias para artigos do blog."""
    __tablename__ = 'article_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#ccc')  # Cor hex
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com artigos
    articles = db.relationship('Article', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<ArticleCategory {self.name}>'

class Article(db.Model):
    """Artigos do blog."""
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)  # Resumo do artigo
    reading_time = db.Column(db.Integer, default=5)  # Tempo de leitura em minutos
    thumbnail_url = db.Column(db.String(200))  # URL da imagem de capa
    is_published = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)  # Destaque
    view_count = db.Column(db.Integer, default=0)  # Contador de visualizações
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Chaves estrangeiras
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('article_categories.id'), nullable=False)
    
    # Relacionamentos
    author = db.relationship('User', backref='articles', lazy=True)
    
    def __repr__(self):
        return f'<Article {self.title}>'
    
    def increment_view(self):
        """Incrementa o contador de visualizações."""
        self.view_count += 1
        db.session.commit()
