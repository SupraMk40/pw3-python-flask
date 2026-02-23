# Importando flask
from flask import Flask, render_template

#Carregando o flask em uma variável
#Declarando variavel no python
#render template é uma função do flask que renderiza um template 

app = Flask(__name__, template_folder='views')
#__name__ é uma variável de ambiente do python que tem o nome do arquivo atual, nesse caso app.py

#criando uma rota para a página inicial
@app.route('/')
#def cria funções em python
def home():
    return render_template('index.html')

@app.route('/games')
def games():
    return render_template('games.html')

@app.route('/consoles')
def consoles():
    return render_template('consoles.html')

#Iniciando o servidor web
if __name__ == '__main__':
    app.run(debug=True)
#Verificando se app.py é o arquivo principal ele inicia o servidor.
