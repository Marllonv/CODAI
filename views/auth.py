from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from extensions import db
from models.users import User
from flask import current_app
from flask_mail import Message
from extensions import mail
from threading import Thread


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


def send_reset_email(user):
    token = user.get_reset_token()
    reset_url = url_for('auth.reset_token', token=token, _external=True)

    subject = 'Redefinição de senha - CODAI'
    html = render_template('auth/reset_email.html', user=user, reset_url=reset_url)

    # Envio assíncrono via Flask-Mail se estiver configurado
    try:
        msg = Message(subject=subject, recipients=[user.email], html=html)
        msg.sender = current_app.config.get('MAIL_USERNAME') or 'no-reply@codai.local'

        def send_async(app, message):
            with app.app_context():
                mail.send(message)

        thr = Thread(target=send_async, args=(current_app._get_current_object(), msg))
        thr.start()
        return True
    except Exception:
        # Se falhar (ex: sem config), fallback para imprimir o link no console
        print(f'[RECOVERY LINK] Para {user.email}: {reset_url}')
        return False


def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('auth.perfil'))

    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        reset_url = None
        if user:
            # Gera o token e tenta enviar o e-mail (se configurado)
            token = user.get_reset_token()
            reset_url = url_for('auth.reset_token', token=token, _external=True)
            send_reset_email(user)

        # Se estivermos em debug ou sem servidor SMTP configurado, mostramos o link na própria página
        mail_configured = bool(current_app.config.get('MAIL_USERNAME'))
        if current_app.debug or not mail_configured:
            # Mostra mensagem informativa e, quando disponível, o link direto
            info = 'Se o e-mail existir em nosso sistema, um link de redefinição foi gerado.'
            flash(info, 'info')
            return render_template('auth/reset_request.html', reset_url=reset_url)

        # Em produção, comportamento neutro: não revelar existência de conta
        flash('Se o e-mail existir em nosso sistema, um link de redefinição foi enviado.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_request.html')


def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('auth.perfil'))

    user = User.verify_reset_token(token)
    if not user:
        flash('O token é inválido ou expirou.', 'error')
        return redirect(url_for('auth.reset_request'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if not password or not confirm:
            flash('Preencha todos os campos.', 'error')
            return render_template('auth/reset_token.html')
        if password != confirm:
            flash('As senhas não coincidem.', 'error')
            return render_template('auth/reset_token.html')

        user.set_password(password)
        db.session.commit()
        flash('Sua senha foi atualizada. Faça login com a nova senha.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_token.html')
