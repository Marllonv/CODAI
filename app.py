from flask import Flask, render_template
from models.users import db, User
from models.forum import Category, Post, Comment
from models.blog import Article, ArticleCategory
from extensions import login_manager
from extensions import mail
from routes.auth import auth_bp
from routes.main import main_bp
from routes.forum import forum_bp
from routes.blog import blog_bp
from models.blog import Article
from models.forum import Post 

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua_chave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codai.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Configurações de e-mail (exemplo). Ajuste com suas credenciais em produção.
    app.config.setdefault('MAIL_SERVER', '')
    app.config.setdefault('MAIL_PORT', 587)
    app.config.setdefault('MAIL_USE_TLS', True)
    app.config.setdefault('MAIL_USERNAME', '')
    app.config.setdefault('MAIL_PASSWORD', '')

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
  
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(forum_bp)
    app.register_blueprint(blog_bp)
    
    with app.app_context(): 
        db.create_all()
        
        # Criar usuário admin se não existir
        master = User.query.filter_by(email="admin@codai.com").first()
        if not master:
            master = User(
                nome="Admin Master",
                email="admin@codai.com",
                role="master"
            )
            master.set_password("123456")
            db.session.add(master)
            db.session.commit()
        
        # Criar categorias padrão se não existirem
        categories_data = [
            {"name": "javascript", "description": "Discussões sobre JavaScript", "color": "#f7df1e"},
            {"name": "react", "description": "React e bibliotecas relacionadas", "color": "#61dafb"},
            {"name": "python", "description": "Python e suas aplicações", "color": "#3776ab"},
            {"name": "frontend", "description": "Desenvolvimento front-end", "color": "#ff6b6b"},
            {"name": "git", "description": "Git e GitHub", "color": "#f05032"},
            {"name": "datascience", "description": "Data Science e análise de dados", "color": "#ff9f43"}
        ]
        
        for cat_data in categories_data:
            if not Category.query.filter_by(name=cat_data["name"]).first():
                category = Category(
                    name=cat_data["name"],
                    description=cat_data["description"],
                    color=cat_data["color"]
                )
                db.session.add(category)
        
        db.session.commit()
        
        # Criar categorias do blog se não existirem
        blog_categories_data = [
            {"name": "javascript", "description": "Artigos sobre JavaScript", "color": "#f7df1e"},
            {"name": "react", "description": "React e bibliotecas relacionadas", "color": "#61dafb"},
            {"name": "python", "description": "Python e suas aplicações", "color": "#3776ab"},
            {"name": "css", "description": "CSS e design", "color": "#1572b6"},
            {"name": "git", "description": "Git e GitHub", "color": "#f05032"},
            {"name": "datascience", "description": "Data Science e análise de dados", "color": "#ff9f43"}
        ]
        
        for cat_data in blog_categories_data:
            if not ArticleCategory.query.filter_by(name=cat_data["name"]).first():
                category = ArticleCategory(
                    name=cat_data["name"],
                    description=cat_data["description"],
                    color=cat_data["color"]
                )
                db.session.add(category)
        
        db.session.commit()
        
        # Criar artigos de exemplo se não existirem
        if not Article.query.first():
            sample_articles = [
                {
                    "title": "Introdução ao JavaScript moderno",
                    "excerpt": "Conceitos essenciais, práticas recomendadas e exercícios para começar a programar com JS.",
                    "content": "JavaScript é uma das linguagens de programação mais populares do mundo. Neste artigo, vamos explorar os conceitos fundamentais que todo desenvolvedor iniciante precisa conhecer.\n\n## Variáveis e Tipos de Dados\n\nJavaScript possui diferentes tipos de dados: strings, numbers, booleans, arrays e objects. Aprender a trabalhar com esses tipos é fundamental.\n\n## Funções\n\nAs funções são blocos de código reutilizáveis que executam uma tarefa específica. Elas são essenciais para organizar e modularizar seu código.\n\n## Conclusão\n\nJavaScript é uma linguagem poderosa e versátil. Com prática constante, você pode dominar seus conceitos e criar aplicações incríveis.",
                    "category_name": "javascript",
                    "reading_time": 7,
                    "is_featured": False
                },
                {
                    "title": "Guia prático de React Hooks",
                    "excerpt": "Entenda useState, useEffect e outros hooks através de exemplos aplicados e fáceis de seguir.",
                    "content": "React Hooks revolucionaram a forma como escrevemos componentes funcionais em React. Neste guia prático, vamos explorar os hooks mais importantes.\n\n## useState\n\nO useState é o hook mais básico e usado para gerenciar estado em componentes funcionais.\n\n```jsx\nconst [count, setCount] = useState(0);\n```\n\n## useEffect\n\nO useEffect permite executar efeitos colaterais em componentes funcionais, similar aos métodos de ciclo de vida em componentes de classe.\n\n## Conclusão\n\nOs hooks tornam o React mais simples e intuitivo. Pratique com projetos reais para dominar esses conceitos.",
                    "category_name": "react",
                    "reading_time": 10,
                    "is_featured": True
                },
                {
                    "title": "Organizando estudos em Python",
                    "excerpt": "Estratégias de estudo, recursos e exercícios para progredir em Python de forma sólida.",
                    "content": "Python é uma linguagem excelente para iniciantes e profissionais. Vamos ver como organizar seus estudos de forma eficiente.\n\n## Fundamentos\n\nComece com os conceitos básicos: variáveis, tipos de dados, estruturas de controle e funções.\n\n## Prática\n\nA prática é essencial. Resolva exercícios, participe de projetos e construa aplicações reais.\n\n## Recursos\n\nExistem muitos recursos gratuitos disponíveis online. Encontre os que funcionam melhor para você.\n\n## Conclusão\n\nCom dedicação e organização, você pode se tornar um desenvolvedor Python proficiente.",
                    "category_name": "python",
                    "reading_time": 6,
                    "is_featured": False
                },
                {
                    "title": "CSS moderno: layout responsivo",
                    "excerpt": "Como usar Grid e Flexbox para criar layouts adaptativos e acessíveis.",
                    "content": "CSS Grid e Flexbox são ferramentas poderosas para criar layouts modernos e responsivos.\n\n## Flexbox\n\nFlexbox é perfeito para layouts unidimensionais. Ele facilita o alinhamento e distribuição de elementos.\n\n## Grid\n\nCSS Grid é ideal para layouts bidimensionais complexos. Ele oferece controle total sobre o posicionamento dos elementos.\n\n## Responsividade\n\nCombine essas ferramentas com media queries para criar layouts que se adaptam a diferentes tamanhos de tela.\n\n## Conclusão\n\nDomine essas técnicas para criar interfaces modernas e acessíveis.",
                    "category_name": "css",
                    "reading_time": 8,
                    "is_featured": False
                },
                {
                    "title": "Controle de versão com Git",
                    "excerpt": "Fluxos de trabalho, boas práticas e comandos essenciais para trabalhar com Git em projetos reais.",
                    "content": "Git é uma ferramenta essencial para desenvolvedores. Vamos aprender os conceitos fundamentais e comandos mais importantes.\n\n## Conceitos Básicos\n\nRepositório, commit, branch e merge são conceitos fundamentais que todo desenvolvedor deve dominar.\n\n## Comandos Essenciais\n\n```bash\ngit add .\ngit commit -m \"Mensagem\"\ngit push origin main\n```\n\n## Fluxos de Trabalho\n\nExistem diferentes fluxos de trabalho como Git Flow e GitHub Flow. Escolha o que funciona melhor para sua equipe.\n\n## Conclusão\n\nGit é uma ferramenta poderosa que melhora significativamente o desenvolvimento em equipe.",
                    "category_name": "git",
                    "reading_time": 9,
                    "is_featured": False
                },
                {
                    "title": "Introdução a Data Science",
                    "excerpt": "Conceitos, ferramentas e um roteiro de aprendizado para começar em ciência de dados.",
                    "content": "Data Science é uma área em crescimento que combina programação, estatística e conhecimento de domínio.\n\n## Fundamentos\n\nComece com Python, pandas, numpy e matplotlib. Essas são as ferramentas básicas da área.\n\n## Estatística\n\nUm bom conhecimento de estatística é fundamental para interpretar dados e tirar conclusões válidas.\n\n## Machine Learning\n\nExplore algoritmos de machine learning para criar modelos preditivos e descobrir padrões nos dados.\n\n## Conclusão\n\nData Science é uma área fascinante que combina várias disciplinas. Comece com os fundamentos e evolua gradualmente.",
                    "category_name": "datascience",
                    "reading_time": 11,
                    "is_featured": False
                }
            ]
            
            for article_data in sample_articles:
                category = ArticleCategory.query.filter_by(name=article_data["category_name"]).first()
                if category:
                    article = Article(
                        title=article_data["title"],
                        content=article_data["content"],
                        excerpt=article_data["excerpt"],
                        reading_time=article_data["reading_time"],
                        is_featured=article_data["is_featured"],
                        author_id=master.id,
                        category_id=category.id
                    )
                    db.session.add(article)
            
            db.session.commit()
        
        if not Post.query.first():
            sample_posts = [
                {
                    "title": "Minha Experiência com JavaScript",
                    "content": "Compartilho aqui como comecei a estudar JavaScript e quais recursos me ajudaram mais nesse processo. Descobri que a prática constante é fundamental para dominar essa linguagem incrível!",
                    "category_name": "javascript",
                    "is_highlighted": False
                },
                {
                    "title": "Dicas para React Iniciantes",
                    "content": "Algumas dicas valiosas para quem está começando com React e quer evitar armadilhas comuns. Foque primeiro nos conceitos básicos antes de partir para bibliotecas mais avançadas.",
                    "category_name": "react",
                    "is_highlighted": True
                },
                {
                    "title": "Como organizar estudos em Python",
                    "content": "Compartilho minha jornada de aprendizado em Python e como organizei meus estudos de forma eficiente. A estruturação é chave para o sucesso!",
                    "category_name": "python",
                    "is_highlighted": False
                },
                {
                    "title": "Recursos gratuitos para Front-end",
                    "content": "Lista com os melhores recursos gratuitos para aprender desenvolvimento front-end em 2023. Há muito conteúdo de qualidade disponível gratuitamente!",
                    "category_name": "frontend",
                    "is_highlighted": False
                },
                {
                    "title": "Desafios com Git e GitHub",
                    "content": "Compartilho os principais desafios que enfrentei ao aprender Git e GitHub e como os superei. A curva de aprendizado pode ser íngreme, mas vale a pena!",
                    "category_name": "git",
                    "is_highlighted": False
                },
                {
                    "title": "Carreira em Data Science",
                    "content": "Minha transição de carreira para Data Science e os principais aprendizados no caminho. Matemática e estatística são fundamentais para esta área.",
                    "category_name": "datascience",
                    "is_highlighted": False
                }
            ]
            
            for post_data in sample_posts:
                category = Category.query.filter_by(name=post_data["category_name"]).first()
                if category:
                    post = Post(
                        title=post_data["title"],
                        content=post_data["content"],
                        user_id=master.id,
                        category_id=category.id,
                        is_highlighted=post_data["is_highlighted"]
                    )
                    db.session.add(post)
            
            db.session.commit()
            
    @app.route("/")
    def home():
        guias = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc()).limit(3).all()
        posts = Post.query.order_by(Post.created_at.desc()).limit(3).all()
        depoimentos = []  # se existir algo a passar

        return render_template(
            "home.html",
            guias=guias,
            posts=posts,
            depoimentos=depoimentos
        )
        

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)