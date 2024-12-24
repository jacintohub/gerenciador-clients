from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flasgger import Swagger

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Inicialização das extensões
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    Swagger(app)  # Documentação Swagger

    # Registro das rotas
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
