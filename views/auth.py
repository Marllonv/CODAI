from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from extensions import db
from models.users import User


# --- Rota: /auth/register ---
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.perfil'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')   # 👈 ADICIONE ESTA LINHA

        # 🧩 Verifica se todos os campos foram preenchidos
        if not nome or not email or not password or not confirm:
            flash('Preencha todos os campos.', 'error')
            return render_template('auth/cadastro.html', nome=nome, email=email)

        # 🧩 Verifica se as senhas coincidem
        if password != confirm:   # 👈 ADICIONE ESTE BLOCO
            flash('As senhas não coincidem.', 'error')
            return render_template('auth/cadastro.html', nome=nome, email=email)

        # Verifica se o e-mail já existe
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Este e-mail já está cadastrado.', 'error')
            return render_template('auth/cadastro.html', nome=nome)

        # Cria novo usuário
        new_user = User(nome=nome, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash(f'Cadastro realizado com sucesso, {nome}. Faça seu login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/cadastro.html')


# --- Rota: /auth/login ---
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.perfil'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Busca o usuário
        user = User.query.filter_by(email=email).first()

        # Verifica credenciais
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f'Bem-vindo de volta, {user.nome}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('auth.perfil'))
        else:
            flash('E-mail ou senha incorretos.', 'error')

    return render_template('auth/login.html')


# --- Rota: /auth/perfil ---
@login_required
def perfil():
    return render_template('auth/perfil.html', user=current_user)


# --- Rota: /auth/logout ---
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login'))
