from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return 'About'

@app.route('/teste/<id>')
def estudante(id):
    return turma[id]

    
turma = {"1": {"nome": "João", "idade": 20, "curso": "Engenharia"},
         "2": {"nome": "Maria", "idade": 22, "curso": "Medicina"},
         "3": {"nome": "José", "idade": 21, "curso": "Direito"},
         "4": {"nome": "Ana", "idade": 23, "curso": "Administração"},
         "5": {"nome": "Pedro", "idade": 24, "curso": "Contabilidade"}}