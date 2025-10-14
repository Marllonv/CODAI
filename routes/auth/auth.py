from . import auth_bp 

from views import auth as auth_view 

# --- Registro Manual das Rotas ---

# Rota para o formulário de cadastro (GET) e envio de dados (POST)
# URL: /auth/register
auth_bp.route('/register', endpoint='register', methods=['GET', 'POST'])(auth_view.register)

# Rota para o formulário de login (GET) e envio de credenciais (POST)
# URL: /auth/login
auth_bp.route('/login', endpoint='login', methods=['GET', 'POST'])(auth_view.login)

# Rota para a visualização do perfil do usuário (GET)
# URL: /auth/perfil
auth_bp.route('/perfil', endpoint='perfil', methods=['GET'])(auth_view.perfil)

# Rota de Logout (POST é mais seguro, mas GET é comum em tutoriais)
# URL: /auth/logout
auth_bp.route('/logout', endpoint='logout', methods=['GET', 'POST'])(auth_view.logout)