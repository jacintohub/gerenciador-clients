import os

class Config:
    # Substituímos o SQLite pelo PostgreSQL (Heroku define a DATABASE_URL automaticamente)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///clientes.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "minha_chave_secreta")
