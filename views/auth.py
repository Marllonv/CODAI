from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# --- Simulação de Extensões e Modelos ---
# NOTA: Em um app real, estes viriam de 'models.users' e 'extensions'
# Exemplo Simulado (assumindo que sua classe User tenha 'email', 'nome' e 'password_hash'):
# from models.users import User, db 
# from app import db 

# Simulação de um banco de dados temporário para que o código seja executável
class MockUser:
    def __init__(self, id, email, nome, role, password_hash):
        self.id = id
        self.email = email
        self.nome = nome
        self.role = role
        self.password_hash = password_hash
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)

# Simulação de um usuário admin criado no app.py 2
MOCK_DB_USERS = {
    1: MockUser(1, "admin@seloedu.com", "Admin Master", "master", generate_password_hash("123456"))
}
USER_ID_COUNTER = 2
# --- Fim da Simulação ---


# Rota: /auth/register (endpoint='auth.register')
def register():
    # 1. Se o usuário já estiver logado, redireciona para o perfil
    if current_user.is_authenticated:
        return redirect(url_for('auth.perfil'))

    if request.method == 'POST':
        # 2. Coleta dados do formulário
        email = request.form.get('email')
        password = request.form.get('password')
        nome = request.form.get('nome')

        # 3. Validação (simples)
        if not email or not password or not nome:
            flash('Preencha todos os campos.', 'error')
            return render_template('auth/cadastro.html', email=email, nome=nome)

        # 4. Simulação: Verifica se o usuário já existe
        if email in [u.email for u in MOCK_DB_USERS.values()]:
            flash('Este e-mail já está cadastrado.', 'error')
            return render_template('auth/cadastro.html', nome=nome)

        # 5. Simulação: Cria novo usuário e salva no "banco"
        global USER_ID_COUNTER
        new_user = MockUser(USER_ID_COUNTER, email, nome, "user", generate_password_hash(password))
        MOCK_DB_USERS[USER_ID_COUNTER] = new_user
        USER_ID_COUNTER += 1
        
        # 6. Redireciona para login
        flash(f'Cadastro realizado com sucesso, {nome}. Faça seu login.', 'success')
        return redirect(url_for('auth.login'))

    # Se for GET, apenas renderiza o template (cadastro.html)
    return render_template('auth/cadastro.html')


# Rota: /auth/login (endpoint='auth.login')
def login():
    # 1. Se o usuário já estiver logado, redireciona para o perfil
    if current_user.is_authenticated:
        return redirect(url_for('auth.perfil'))

    if request.method == 'POST':
        # 2. Coleta dados
        email = request.form.get('email')
        password = request.form.get('password')

        # 3. Simulação: Busca usuário no "banco"
        user = next((u for u in MOCK_DB_USERS.values() if u.email == email), None)

        # 4. Verifica usuário e senha
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True) # Faz o login com Flask-Login
            flash(f'Bem-vindo de volta, {user.nome}!', 'success')
            
            # Pega o próximo destino (se houver, ex: após tentar acessar uma página restrita)
            next_page = request.args.get('next')
            # Redireciona para o destino ou para o perfil
            return redirect(next_page or url_for('auth.perfil'))
        else:
            flash('Login inválido. Verifique seu e-mail e senha.', 'error')

    # Se for GET, apenas renderiza o template (login.html)
    return render_template('auth/login.html')


# Rota: /auth/perfil (endpoint='auth.perfil')
@login_required # Garante que só usuários logados acessem
def perfil():
    # Renderiza o template de perfil, passando os dados do usuário logado
    return render_template('auth/perfil.html', user=current_user)


# Rota: /auth/logout (endpoint='auth.logout')
@login_required 
def logout():
    # Finaliza a sessão do usuário com Flask-Login
    logout_user()
    flash('Você foi desconectado com sucesso.', 'success')
    # Redireciona para a página de login ou para a home
    return redirect(url_for('auth.login'))