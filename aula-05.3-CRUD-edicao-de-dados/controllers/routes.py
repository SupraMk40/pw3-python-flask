# Importando o render_template
# Motor para renderizar as páginas
from flask import render_template, request, redirect, url_for
from models.database import Game, Console, db
# Criando a função para receber o Flask (app)


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
        console = Console.query.all()
        #redirecionando o usuario para a pagina de estoque
        return render_template('estoque-consoles.html', console=Console)