from flask import render_template

def home():
    """Lógica para a página inicial."""
    return render_template("home.html")

def forum():
    """Lógica para a página do fórum."""
    return render_template("forum.html")

def blog():
    """Lógica para a página do blog."""
    return render_template("blog.html")