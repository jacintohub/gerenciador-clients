from . import db

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))
    status_pagamento = db.Column(db.String(20), nullable=False)  # Ex.: pago, pendente
    data_contratacao = db.Column(db.Date, nullable=False)

    # Relacionamento com Site
    sites = db.relationship("Site", backref="cliente", lazy=True)

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    dominio = db.Column(db.String(100), unique=True, nullable=False)
    hospedagem = db.Column(db.String(100))
    data_vencimento_hospedagem = db.Column(db.Date)
    login_hospedagem_usuario = db.Column(db.String(100))
    login_hospedagem_senha = db.Column(db.String(100))
    login_painel_wordpress_usuario = db.Column(db.String(100))
    login_painel_wordpress_senha = db.Column(db.String(100))
