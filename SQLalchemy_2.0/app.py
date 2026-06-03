from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy # feito

app = Flask(__name__)

# feito
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///loja.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# feito
db = SQLAlchemy(app)


# feito
class Produto(db.Model):
__tablename__ = "produtos"

id = db.Column(db.Integer, primary_key=True)
nome = db.Column(db.String(120), nullable=False)
categoria = db.Column(db.String(60), nullable=False)
preco = db.Column(db.Float, nullable=False)
estoque = db.Column(db.Integer, nullable=False)

def __repr__(self):
return f"<Produto {self.nome}>"


# feito
with app.app_context():
db.create_all()


@app.route("/")
def lista_produtos():
# feito
produtos = Produto.query.order_by(Produto.nome).all()
return render_template("lista.html", produtos=produtos)


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
erro = None

if request.method == "POST":
nome = request.form.get("nome", "").strip()
categoria = request.form.get("categoria", "").strip()

try:
preco = float(request.form.get("preco", 0))
except:
preco = 0

try:
estoque = int(request.form.get("estoque", 0))
except:
estoque = -1

# feito
if not nome or not categoria:
erro = "Nome e categoria são obrigatórios."
elif preco <= 0:
erro = "Preço deve ser maior que zero."
elif estoque < 0:
erro = "Estoque não pode ser negativo."
else:
produto = Produto(
nome=nome,
categoria=categoria,
preco=preco,
estoque=estoque
)

# feito
db.session.add(produto)
db.session.commit()

return redirect(url_for("lista_produtos"))

return render_template("formulario.html", produto=None, erro=erro)


@app.route("/editar/<int:produto_id>", methods=["GET", "POST"])
def editar(produto_id):
# feito
produto = Produto.query.get_or_404(produto_id)

erro = None

if request.method == "POST":
nome = request.form.get("nome", "").strip()
categoria = request.form.get("categoria", "").strip()

try:
preco = float(request.form.get("preco", 0))
except:
preco = 0

try:
estoque = int(request.form.get("estoque", 0))
except:
estoque = -1

# feito
if not nome or not categoria:
erro = "Nome e categoria são obrigatórios."
elif preco <= 0:
erro = "Preço deve ser maior que zero."
elif estoque < 0:
erro = "Estoque não pode ser negativo."
else:
produto.nome = nome
produto.categoria = categoria
produto.preco = preco
produto.estoque = estoque

# feito
db.session.commit()

return redirect(url_for("lista_produtos"))

return render_template("formulario.html", produto=produto, erro=erro)


@app.route("/excluir/<int:produto_id>", methods=["POST"])
def excluir(produto_id):
# feito
produto = Produto.query.get_or_404(produto_id)

db.session.delete(produto)
db.session.commit()

return redirect(url_for("lista_produtos"))


if __name__ == "__main__":
app.run(debug=True)