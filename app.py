from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page1')
def page1():
    return render_template('sobremim.html')

@app.route('/page2')
def page2():
    return render_template('sobreaulas.html')

@app.route('/page3')
def page3():
    return render_template('sobreti.html')

if __name__ == '__main__':
    app.run(debug=True)