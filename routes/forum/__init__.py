from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.forum import Post, Category, Comment
from models.users import User
from extensions import db
from datetime import datetime

forum_bp = Blueprint('forum', __name__, url_prefix='/forum')

@forum_bp.route('/')
def index():
    """Página principal do fórum com todos os posts."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('forum.html', posts=posts, categories=categories)

@forum_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Criar um novo post."""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        is_highlighted = bool(request.form.get('is_highlighted'))
        
        if not title or not content or not category_id:
            flash('Todos os campos são obrigatórios!', 'error')
            return redirect(url_for('forum.create_post'))
        
        post = Post(
            title=title,
            content=content,
            user_id=current_user.id,
            category_id=category_id,
            is_highlighted=is_highlighted
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Post criado com sucesso!', 'success')
        return redirect(url_for('forum.index'))
    
    categories = Category.query.all()
    return render_template('forum/create_post.html', categories=categories)

@forum_bp.route('/post/<int:post_id>')
def view_post(post_id):
    """Visualizar um post específico."""
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()
    return render_template('forum/post_detail.html', post=post, comments=comments)

@forum_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Editar um post."""
    post = Post.query.get_or_404(post_id)
    
    # Verificar se o usuário pode editar o post
    if post.user_id != current_user.id and current_user.role != 'master':
        flash('Você não tem permissão para editar este post!', 'error')
        return redirect(url_for('forum.view_post', post_id=post_id))
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.category_id = request.form.get('category_id')
        post.is_highlighted = bool(request.form.get('is_highlighted'))
        post.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Post atualizado com sucesso!', 'success')
        return redirect(url_for('forum.view_post', post_id=post_id))
    
    categories = Category.query.all()
    return render_template('forum/edit_post.html', post=post, categories=categories)

@forum_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Deletar um post."""
    post = Post.query.get_or_404(post_id)
    
    # Verificar se o usuário pode deletar o post
    if post.user_id != current_user.id and current_user.role != 'master':
        flash('Você não tem permissão para deletar este post!', 'error')
        return redirect(url_for('forum.view_post', post_id=post_id))
    
    db.session.delete(post)
    db.session.commit()
    flash('Post deletado com sucesso!', 'success')
    return redirect(url_for('forum.index'))

@forum_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """Adicionar comentário a um post."""
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    
    if not content:
        flash('O comentário não pode estar vazio!', 'error')
        return redirect(url_for('forum.view_post', post_id=post_id))
    
    comment = Comment(
        content=content,
        user_id=current_user.id,
        post_id=post_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('Comentário adicionado com sucesso!', 'success')
    return redirect(url_for('forum.view_post', post_id=post_id))

@forum_bp.route('/category/<int:category_id>')
def posts_by_category(category_id):
    """Posts filtrados por categoria."""
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category_id=category_id).order_by(Post.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('forum.html', posts=posts, categories=categories, selected_category=category)

@forum_bp.route('/api/posts')
def api_posts():
    """API endpoint para buscar posts (para AJAX)."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    posts_data = []
    
    for post in posts:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
            'author': post.user.nome,
            'category': post.category.name,
            'category_color': post.category.color,
            'created_at': post.created_at.strftime('%d/%m/%Y %H:%M'),
            'is_highlighted': post.is_highlighted,
            'comments_count': len(post.comments)
        })
    
    return jsonify(posts_data)
