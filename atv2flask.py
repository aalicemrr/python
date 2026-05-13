from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def curriculo():
    data = {
        "nome": "João Silva",
        "telefone": "(11) 99999-9999",
        "email": "joao.silva@email.com",
        "educacao": [
            {"instituicao": "Universidade XYZ", "curso": "Bacharelado em Ciência da Computação", "ano": "2018 - 2022"},
            {"instituicao": "Escola Técnica ABC", "curso": "Técnico em Informática", "ano": "2016 - 2017"}
        ],
        "experiencia": [
            {"cargo": "Desenvolvedor Python Júnior", "empresa": "Tech Solutions", "periodo": "Jan 2023 - Presente", "desc": "Desenvolvimento de APIs com Flask e automação de scripts."},
            {"cargo": "Estagiário de TI", "empresa": "Web Innovate", "periodo": "Jun 2022 - Dez 2022", "desc": "Suporte técnico e manutenção de bancos de dados."}
        ],
        "cursos": [
            "Curso Intensivo de Flask - Udemy",
            "Certificação AWS Cloud Practitioner",
            "Inglês para Negócios - Cultura Inglesa"
        ],
        "idiomas": {
            "Inglês": "Avançado",
            "Espanhol": "Intermediário"
        }
    }
    return render_template('cv.html', cv=data)

if __name__ == '__main__':
    app.run(debug=True)
