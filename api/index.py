from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient

load_dotenv(find_dotenv())
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()
uri = os.getenv('MONGODB_URI')
db = MongoClient(uri, ssl=True, tlsAllowInvalidCertificates=True)['mjd_2024']

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/incluir')
def incluir():
    return render_template('incluir.html')

@app.route('/sucesso', methods=['POST'])
def sucesso():
    termo_br = request.form.get('termo_br')
    termo_en = request.form.get('termo_en')
    novos_dados = {'termo_portugues': termo_br, 'traducao': termo_en}
    db.joao_tradutor.insert_one(novos_dados)
    return 'Enviado com sucesso.'

@app.route('/tradutor', methods=['GET', 'POST'])
def traducao():
    dicionario = db.joao_tradutor
    palavras = [x for x in dicionario.find()]
    dicionario_final = {}
    for termo in palavras:
        dicionario_final[termo['termo_portugues']] = termo['traducao']

    texto = request.form.get('texto_a_traduzir')
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Traduza o seguinte texto para inglês, mas considere o valor do\
            dicionário {dicionario_final} como tradução para as palavras que estiverem nas chaves desse mesmo dicionário. Não faça nenhum tipo de interação com o usuário.\
            Apenas traduza o texto que ele inserir."},
            {"role": "user", "content": texto}
        ],
        temperature=0.6,
        top_p=1
    )
    return render_template('tradutor.html', resultado = response.choices[0].message.content)    
    
