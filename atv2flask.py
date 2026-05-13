from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def curriculo():
    data = {
        "nome": "Alice Araujo",
        "telefone": "(31) 98204-6078",
        "email": "alice.araujo@email.com",
        "educacao": [
            {"instituicao": "Colegio Técnico Cotemig", "curso": "Técnico em Informática", "ano": "2024 - 2026"}
        ],
        "experiencia": [
            {"cargo": "Estagiário de TI", "empresa": "Web Innovate", "periodo": "Jun 2025 - Dez 2025", "desc": "Suporte técnico e manutenção de bancos de dados."}
        ],
        "cursos": [
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


'''<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currículo - {{ cv.nome }}</title>
    <link href="https://jsdelivr.net" rel="stylesheet">
    <style>
        body { background-color: #f4f7f6; }
        .cv-container { max-width: 800px; margin: 30px auto; background: #fff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; }
        h4 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 20px; }
        .contact-info { font-size: 0.9rem; color: #7f8c8d; }
        .experience-item, .education-item { margin-bottom: 15px; }
    </style>
</head>
<body>

<div class="container">
    <div class="cv-container">
        <div class="text-center">
            <h1>{{ cv.nome }}</h1>
            <p class="contact-info">
                📞 {{ cv.telefone }} | ✉️ {{ cv.email }}
            </p>
        </div>

        <h4>Educação</h4>
        {% for edu in cv.educacao %}
        <div class="education-item">
            <strong>{{ edu.instituicao }}</strong> - {{ edu.curso }}<br>
            <small class="text-muted">{{ edu.ano }}</small>
        </div>
        {% endfor %}

        <h4>Experiência Profissional</h4>
        {% for exp in cv.experiencia %}
        <div class="experience-item">
            <strong>{{ exp.cargo }}</strong> na <em>{{ exp.empresa }}</em><br>
            <small class="text-muted">{{ exp.periodo }}</small>
            <p>{{ exp.desc }}</p>
        </div>
        {% endfor %}


        <h4>Cursos e Certificações</h4>
        <ul>
            {% for curso in cv.cursos %}
            <li>{{ curso }}</li>
            {% endfor %}
        </ul>

        <h4>Idiomas</h4>
        <ul>
            {% for idioma, nivel in cv.idiomas.items() %}
            <li><strong>{{ idioma }}:</strong> {{ nivel }}</li>
            {% endfor %}
        </ul>

    </div>
</div>

</body>
</html>'''