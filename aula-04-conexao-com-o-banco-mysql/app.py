# Importando flask
from flask import Flask, render_template, request
from controllers import routes
import pymysql 
from models.database import db, Game
#Carregando o flask em uma variável
#Declarando variavel no python
#render template é uma função do flask que renderiza um template 

app = Flask(__name__, template_folder='views')
#__name__ é uma variável de ambiente do python que tem o nome do arquivo atual, nesse caso app.py

DB_NAME = 'thegameawards'

app.config['DATABASE_NAME'] = DB_NAME
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'

#enviando a variavel APP Flask para as rotas
routes.init_app(app)
#Iniciando o servidor web
if __name__ == '__main__':
    # passando os dados e criando uma conexao com o bando
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.
                                 cursors.DictCursor)
    
try:
    with connection.cursor () as cursors:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS{DB_NAME}")
        print("Banco criado com sucesso")
except Exception as error:
    print(f"Erro da minha cabeça kkkkkkk: {error}")
finally:
    connection.close()
    
db.init_app(app=app)
with app.test_request_context():
    db.create_all()
    app.run(debug=True)
#Verificando se app.py é o arquivo principal ele inicia o servidor.