# Importando flask
from flask import Flask, render_template, request
from controllers import routes

#Carregando o flask em uma variável
#Declarando variavel no python
#render template é uma função do flask que renderiza um template 

app = Flask(__name__, template_folder='views')
#__name__ é uma variável de ambiente do python que tem o nome do arquivo atual, nesse caso app.py

#enviando a variavel APP Flask para as rotas
routes.init_app(app)
#Iniciando o servidor web
if __name__ == '__main__':
    app.run(debug=True)
#Verificando se app.py é o arquivo principal ele inicia o servidor.