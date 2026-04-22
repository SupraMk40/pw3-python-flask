# pip install flask-sqlalchemy
# Permite conexao com o banco mysql
# pip install pymysql
# Permite a criacao dos models

from flask_sqlalchemy import SQLAlchemy
# Criando uma instancia do SQLAlchemy e carregando em uma variavel
db = SQLAlchemy()
# Criando uma classe para representar a entidade games no banco de dados (tabela: games)
class Game(db.model):
    # colunas da tabela
    id = db.column(db.Integer, primary_key=True)
    titulo = db.column(db.String(150))
    ano = db.column(db.Integer)
    categoria = db.column(db.String(150))
    plataforma = db.column(db.String(150))
    preco = db.column(db.Float)
    quantidade = db.column(db.Integer)

#Metodo construtor (atributos que serao utilizados pelo objeto)
def __init__(self, titulo, ano, categoria, plataforma, preco, quantidade):
    self.titulo = titulo
    self.ano = ano
    self.categoria = categoria
    self.plataforma = plataforma
    self.preco = preco
    self.quantidade = quantidade