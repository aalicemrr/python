from flask import Flask


app = Flask(__name__) # inicio o flask

@app.route('/') # Isso é o decorator, ele é usado para mapear a função abaixo para a rota '/'
def ola_mundo():
    return 'Decorator, oque é?' # Isso é o que será retornado quando a rota '/' for acessada

@app.route('/decorator') # Isso é outro decorator, mapeando a função abaixo para a rota '/hello'
def hello():
    return 'Decorators são um padrão de projeto estrutural, comuns em linguagens como Python e TypeScript, que permitem adicionar novos comportamentos a objetos, métodos ou classes existentes de forma dinâmica, sem alterar o código-fonte original. Eles "embrulham" o código original, permitindo executar ações antes ou depois da sua execução.' # Isso é o que será retornado quando a rota '/hello' for acessada

if __name__ == '__main__':
    app.run(debug=True) # Isso inicia o servidor Flask em modo de depuração, o que é útil para desenvolvimento