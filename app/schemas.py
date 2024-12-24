from . import ma
from .models import Cliente, Site
from marshmallow import validates, ValidationError
import re

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        load_instance = True

    sites = ma.Nested("SiteSchema", many=True)

    @validates("email")
    def validate_email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValidationError("Endereço de e-mail inválido.")

    @validates("telefone")
    def validate_telefone(self, value):
        if not re.match(r"^\d{9,15}$", value):
            raise ValidationError("Telefone deve conter apenas números (9-15 dígitos).")

class SiteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Site
        load_instance = True
