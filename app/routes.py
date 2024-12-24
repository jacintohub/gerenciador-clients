from flask import Blueprint, jsonify, request, Response
from .models import Cliente, Site
from .schemas import ClienteSchema, SiteSchema
from . import db
import json

bp = Blueprint("main", __name__)

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)
site_schema = SiteSchema()
sites_schema = SiteSchema(many=True)

@bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Bem-vindo ao Gerenciador de Clientes!"})

@bp.route("/clientes", methods=["GET"])
def listar_clientes():
    """
    Lista todos os clientes cadastrados com busca e ordenação
    ---
    parameters:
      - name: search
        in: query
        type: string
        description: Termo de busca por nome ou e-mail
      - name: order_by
        in: query
        type: string
        description: Campo para ordenar (nome, email, etc.)
      - name: direction
        in: query
        type: string
        description: Direção da ordenação (asc ou desc)
    responses:
      200:
        description: Lista de clientes
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    search = request.args.get("search", "")
    order_by = request.args.get("order_by", "id")
    direction = request.args.get("direction", "asc")

    query = Cliente.query
    if search:
        query = query.filter(
            Cliente.nome.ilike(f"%{search}%") | Cliente.email.ilike(f"%{search}%")
        )

    if direction == "asc":
        query = query.order_by(getattr(Cliente, order_by).asc())
    else:
        query = query.order_by(getattr(Cliente, order_by).desc())

    paginated_clientes = query.paginate(page=page, per_page=per_page, error_out=False)
    return Response(
        json.dumps({
            "total": paginated_clientes.total,
            "page": paginated_clientes.page,
            "per_page": paginated_clientes.per_page,
            "clientes": clientes_schema.dump(paginated_clientes.items),
        }, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )

@bp.route("/clientes/<int:cliente_id>/sites", methods=["GET"])
def listar_sites_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    return jsonify(sites_schema.dump(cliente.sites))

@bp.route("/clientes/<int:cliente_id>/sites", methods=["POST"])
def criar_site(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    data = request.json
    novo_site = site_schema.load(data, session=db.session)
    novo_site.cliente_id = cliente.id
    db.session.add(novo_site)
    db.session.commit()
    return jsonify(site_schema.dump(novo_site)), 201

@bp.route("/clientes", methods=["POST"])
def criar_cliente():
    data = request.json
    novo_cliente = cliente_schema.load(data, session=db.session)
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify(cliente_schema.dump(novo_cliente)), 201

@bp.route("/clientes/<int:cliente_id>", methods=["PUT"])
def atualizar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    data = request.json
    for key, value in data.items():
        setattr(cliente, key, value)
    db.session.commit()
    return jsonify(cliente_schema.dump(cliente)), 200

@bp.route("/clientes/<int:cliente_id>", methods=["DELETE"])
def excluir_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": f"Cliente {cliente.nome} excluído com sucesso."}), 200
