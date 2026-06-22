
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .cliente import Cliente
from .pedido import ItemPedido, Pedido
from .cliente_locadora import ClienteLocadora
from .veiculo import Veiculo
from .locacao import Locacao

__all__ = [
    "db", "ModeloBase",
    "Cliente", "Pedido", "ItemPedido",
    "ClienteLocadora", "Veiculo", "Locacao",
]
