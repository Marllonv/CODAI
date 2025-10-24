from flask import render_template
from models.forum import Post, Category
from models.blog import Article, ArticleCategory

def home():
    """Lógica para a página inicial."""
    return render_template("home.html")

def forum():
    """Lógica para a página do fórum."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    categories = Category.query.all()
    return render_template("forum.html", posts=posts, categories=categories)

def blog():
    """Lógica para a página do blog."""
    articles = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc()).all()
    categories = ArticleCategory.query.all()
    return render_template("blog.html", articles=articles, categories=categories)