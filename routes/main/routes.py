#routes/main/routes.py
from . import main_bp 
from views import main as main_view 


# --- Registro Manual das Rotas Principais (Main Blueprint) ---

# Rota: / (Home)    
# Endpoint: main.home
main_bp.route('/', endpoint='home', methods=['GET'])(main_view.home)

# Rota: /forum
# Endpoint: main.forum
main_bp.route('/forum', endpoint='forum', methods=['GET'])(main_view.forum)

# Rota: /blog
# Endpoint: main.blog
main_bp.route('/blog', endpoint='blog', methods=['GET'])(main_view.blog)