# Importando o render_template
# Motor para renderizar as páginas
from flask import render_template, request, redirect, url_for, flash
# Importando o Markup Safe, que permite voce adicionar links na flash message
from markupsafe import Markup
from models.database import Game, Console, db, Usuario
# Criando a função para receber o Flask (app)
from werkzeug.security import generate_password_hash
#Importando URLLIB
import urllib.request #Permite enviar requisições para uma url
#Importando JSON
import json #Converte dados de dicionario para JSON

def init_app(app):
    # SIMULANDO UM BANCO DE DADOS
    listaGames = [{"titulo": "CS-GO", "ano": 2012, "categoria": "FPS Online"}]

    # A partir daqui virão as rotas

    # CRIANDO A ROTA PRINCIPAL DO SITE
    @app.route('/')
    # def serve para criar funções no Python
    def home():
        return render_template('index.html')

    # CRIANDO A ROTA DE GAMES
    @app.route('/games')
    def games():
        # Criando variáveis para passar as informações de um jogo
        titulo = "Silk Song"
        ano = 2025
        categoria = "Metroid Van"

        # Criando um objeto Python (dicionário) para representar as propriedades de um jogo
        game = {
            "Título": "Minecraft",
            "Ano": 2012,
            "Categoria": "Sandbox"
        }
        # Criando vetor (lista)
        jogadores = ['Eduardo', 'Ana', 'Guilherme', 'Vitor', 'Antônio']
        return render_template('games.html',
                               # Enviando as variáveis para página HTML
                               titulo=titulo,
                               ano=ano,
                               categoria=categoria,
                               jogadores=jogadores,
                               game=game)

    # CRIANDO A ROTA DE CONSOLES
    @app.route('/consoles')
    def consoles():
        # Criando vetor (lista)
        consoles = ['Xbox', 'Playstation 5',
                    'Super Nintendo', 'Gameboy', 'Atari']
        return render_template('consoles.html',
                               consoles=consoles)

    # ROTA DE CADASTRO DE JOGOS
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        # Verificando se o método da requisição é POST
        if request.method == 'POST':
            # Recebendo os dados do formulário e gravando na lista
            listaGames.append({'titulo' : request.form.get('titulo'), 'ano' : request.form.get('ano'), 'categoria' : request.form.get('categoria')})
            # o método append() adiciona valores a lista
            return redirect(url_for('cadgames'))    
        return render_template('cadgames.html',
                               listaGames = listaGames)

    @app.route("/estoque-jogos", methods=['GET', 'POST'])
    #criando um parametro na rota
    @app.route("/estoque-jogos/delete/<int:id>")
    def estoque_jogos(id=None):
        #Verificando se esta sendo enviado o parametro ID para a rota
        if id:
            game = Game.query.get(id)#select no banco #deleta o jogo
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque_jogos'))
        
        #Verificando se a requisição é do tipo post
        if request.method == 'POST':
            #colentando os dados preenchidos no formulario
            dados_form = request.form.to_dict()
            #enviando os dados para o model
            newGame = Game(
                dados_form['titulo'],
                dados_form['ano'],
                dados_form['categoria'], 
                dados_form['plataforma'],
                dados_form['preco'],
                dados_form['quantidade']
            )
            #metodo SQLAlchemy para gravar os dados do banco
            db.session.add(newGame)
            #confirmando a operação no banco
            db.session.commit()
            return redirect(url_for('estoque_jogos'))
        #selecionando rodos os jogos do banco
        #SELECT * FROM GAMES
        games = Game.query.all()
        #redirecionando o usuario para a pagina de estoque
        return render_template('estoque-jogos.html', games=games)
        
    @app.route('/editar-jogos/<int:id>', methods=['GET', 'POST'])
    def editar_jogos(id):
        game = Game.query.get(id)
        if request.method == 'POST':
            dados_form = request.form.to_dict()
            game.titulo = dados_form['titulo']
            game.ano = dados_form['ano']
            game.categoria = dados_form['categoria']
            game.plataforma = dados_form['plataforma']
            game.preco = dados_form['preco']
            game.quantidade = dados_form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editar-jogos.html', game=game)
            

    
    @app.route("/estoque-consoles", methods=['GET', 'POST'])
    #criando um parametro na rota
    @app.route("/estoque-consoles/delete/<int:id>")
    def estoque_consoles(id=None):
        #Verificando se esta sendo enviado o parametro ID para a rota
        if id:
            game = Console.query.get(id)#select no banco #deleta o jogo
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque_consoles'))
        
        #Verificando se a requisição é do tipo post
        if request.method == 'POST':
            #colentando os dados preenchidos no formulario
            dados_form = request.form.to_dict()
            #enviando os dados para o model
            newConsole = Console(
                dados_form['nome'],
                dados_form['fabricante'],
                dados_form['ano'], 
                dados_form['preco'],
                dados_form['quantidade']
            )
            #metodo SQLAlchemy para gravar os dados do banco
            db.session.add(newConsole)
            #confirmando a operação no banco
            db.session.commit()
            return redirect(url_for('estoque_consoles'))
            
        #selecionando rodos os jogos do banco
        #SELECT * FROM GAMES
        consoles = Console.query.all()
        #redirecionando o usuario para a pagina de estoque
        return render_template('estoque-consoles.html', consoles=consoles)
    
    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro():
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario:
                msg = Markup("Usuário já cadastrado, ta de brincadeira comigo mano? Aqui é pra fazer <a href='/login'>login</a>...")
                flash(msg, 'danger')
                return redirect(url_for('cadastro'))
            
            senha_criptografia = generate_password_hash(senha, method='scrypt')
            
            novo_usuario = Usuario(email=email, senha=senha_criptografia)
            db.session.add(novo_usuario)
            db.session.commit()
            msgCad = Markup("Cadastro realizado com sucesso! faça o <a href='/login'>login</a>")
            flash(msgCad, 'success')
            
            return redirect(url_for('cadastro'))
        return render_template('cadastro.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return render_template('login.html')
    
    #Rota de consumo da API
    @app.route('/apigames', methods=['GET', 'POST'])
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        urlAPI = 'https://www.freetogame.com/api/games'
        #Enviando requisição para api
        resposta = urllib.request.urlopen(urlAPI)
        #Lendo os dados
        dados = resposta.read()
        #Convertendo dados de JSON para DICIONARIO
        listaJogos = json.loads(dados)
        #verificando se a rota nao desrecebeu a id
        if id:
            jogoInfo = []
            for jogo in listaJogos:
                if jogo['id'] == id:
                    jogoInfo = jogo
                    break
            if jogoInfo:
                return render_template('gameinfo.html', jogoInfo=jogoInfo)
            else:
                return f'Seu animal, ta tentando burlar o sistema? A id {id} não existe cara!!'
        else:
            return render_template('apigames.html', listaJogos=listaJogos)
        return render_template('apigames.html',
                               listaJogos=listaJogos)