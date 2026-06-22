
from . import db
from .base import ModeloBase


class Cliente(ModeloBase):
    __tablename__ = "clientes"

    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)

    pedidos = db.relationship("Pedido", back_populates="cliente", lazy=True)

    
    @classmethod
    def listar_ordenados(cls):
        return cls.query.order_by(cls.nome).all()

    @classmethod
    def salvar(cls, nome, email, telefone=""):
        
        cliente = cls(nome=nome, email=email, telefone=telefone or None)
        db.session.add(cliente)
        db.session.commit()
        return cliente

   
    def atualizar(self, nome, email, telefone=""):
        self.nome = nome
        self.email = email
        self.telefone = telefone or None
        db.session.commit()

    def excluir(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Cliente {self.id} {self.nome}>"
