from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.blog import Article, ArticleCategory
from models.users import User
from extensions import db
from datetime import datetime

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

@blog_bp.route('/')
def index():
    """Página principal do blog com todos os artigos."""
    articles = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc()).all()
    categories = ArticleCategory.query.all()
    return render_template('blog.html', articles=articles, categories=categories)

@blog_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_article():
    """Criar um novo artigo."""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        category_id = request.form.get('category_id')
        reading_time = request.form.get('reading_time', 5)
        is_featured = 'is_featured' in request.form
        
        if not title or not content or not category_id:
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'error')
            return redirect(url_for('blog.create_article'))
        
        article = Article(
            title=title,
            content=content,
            excerpt=excerpt,
            reading_time=int(reading_time),
            is_featured=is_featured,
            author_id=current_user.id,
            category_id=int(category_id)
        )
        
        db.session.add(article)
        db.session.commit()
        
        flash('Artigo criado com sucesso!', 'success')
        return redirect(url_for('blog.view_article', article_id=article.id))
    
    categories = ArticleCategory.query.all()
    return render_template('blog/create_article.html', categories=categories)

@blog_bp.route('/article/<int:article_id>')
def view_article(article_id):
    """Ver um artigo específico."""
    article = Article.query.get_or_404(article_id)
    
    if article.is_published or (current_user.is_authenticated and (current_user.id == article.author_id or current_user.role == 'master')):
        article.increment_view()
        return render_template('blog/article_detail.html', article=article)
    else:
        flash('Artigo não encontrado.', 'error')
        return redirect(url_for('blog.index'))

@blog_bp.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    """Editar um artigo."""
    article = Article.query.get_or_404(article_id)
    
    # Verificar permissões
    if current_user.id != article.author_id and current_user.role != 'master':
        flash('Você não tem permissão para editar este artigo.', 'error')
        return redirect(url_for('blog.view_article', article_id=article_id))
    
    if request.method == 'POST':
        article.title = request.form.get('title')
        article.content = request.form.get('content')
        article.excerpt = request.form.get('excerpt')
        article.category_id = int(request.form.get('category_id'))
        article.reading_time = int(request.form.get('reading_time', 5))
        article.is_featured = 'is_featured' in request.form
        article.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Artigo atualizado com sucesso!', 'success')
        return redirect(url_for('blog.view_article', article_id=article.id))
    
    categories = ArticleCategory.query.all()
    return render_template('blog/edit_article.html', article=article, categories=categories)

@blog_bp.route('/article/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_article(article_id):
    """Deletar um artigo."""
    article = Article.query.get_or_404(article_id)
    
    # Verificar permissões
    if current_user.id != article.author_id and current_user.role != 'master':
        flash('Você não tem permissão para deletar este artigo.', 'error')
        return redirect(url_for('blog.index'))
    
    db.session.delete(article)
    db.session.commit()
    
    flash('Artigo deletado com sucesso!', 'success')
    return redirect(url_for('blog.index'))

@blog_bp.route('/category/<int:category_id>')
def articles_by_category(category_id):
    """Listar artigos por categoria."""
    category = ArticleCategory.query.get_or_404(category_id)
    articles = Article.query.filter_by(category_id=category_id, is_published=True).order_by(Article.created_at.desc()).all()
    categories = ArticleCategory.query.all()
    
    return render_template('blog.html', articles=articles, categories=categories, selected_category=category)

@blog_bp.route('/search')
def search():
    """Buscar artigos por título ou conteúdo."""
    query = request.args.get('q', '').strip()
    
    if query:
        articles = Article.query.filter(
            Article.is_published == True,
            (Article.title.contains(query) | Article.content.contains(query))
        ).order_by(Article.created_at.desc()).all()
    else:
        articles = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc()).all()
    
    categories = ArticleCategory.query.all()
    return render_template('blog.html', articles=articles, categories=categories, search_query=query)

@blog_bp.route('/api/articles')
def api_articles():
    """API para retornar artigos em JSON."""
    articles = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc()).all()
    
    articles_data = []
    for article in articles:
        articles_data.append({
            'id': article.id,
            'title': article.title,
            'excerpt': article.excerpt,
            'author': article.author.nome,
            'category': article.category.name,
            'category_color': article.category.color,
            'reading_time': article.reading_time,
            'created_at': article.created_at.isoformat(),
            'view_count': article.view_count,
            'is_featured': article.is_featured
        })
    
    return jsonify(articles_data)
