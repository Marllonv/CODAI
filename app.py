from flask import Flask, render_template
from models.users import db, User
from extensions import login_manager
from routes.auth import auth_bp
from routes.main import main_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua_chave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codai.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    with app.app_context(): 
        db.create_all()
        if not User.query.filter_by(email="admin@codai.com").first():
            master = User(
                nome="Admin Master",
                email="admin@codai.com",
                role="master"
            )
            master.set_password("123456")
            db.session.add(master)
            db.session.commit()
    @app.route("/")
    def home():
        posts = []
        guias = []
        depoimentos = []

        return render_template(
            "home.html",
            posts=posts,
            guias=guias,
            depoimentos=depoimentos
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)