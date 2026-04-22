#motor para renderizar as paginas
from flask import render_template, request, redirect, url_for

#criando função para receber o flask(app)
def init_app(app):
    #as rotas virao a partir daqui
    listaGames = [{"titulo": "CS2", "ano" : 2022, "categoria" : "Aventura"}]    
    #criando uma rota para a página inicial
    @app.route('/')
    #def cria funções em python
    def home():
        return render_template('index.html')

    @app.route('/games')
    def games():
        #Criando um vetor (lista)
        jogadores = ['Eduardo', 'Ana', 'Guilherme', 'Vitor', 'Antônio']
        
        #criando um objeto python para representar as propriedades de um jogo
        game = {
            'Titulo': 'Forza Horizon 6',
            'Ano': 2026,
            'Categoria': 'Corrida'
        }
        
        #criando variaveis para passar informações de um jogo
        titulo = "Forza Horizon 6"
        ano = 2026
        categoria = "Corrida"
        return render_template('games.html',
                            #enviando as variaveis
                            titulo=titulo,
                            ano=ano,
                            categoria=categoria,
                            jogadores=jogadores,
                            game=game)
        

    @app.route('/consoles')
    def consoles():
        consoles = ['Xbox Series A', 'Xbox Series B', 'Playstation 6', 'Playstation 7', 'Mobile']
        return render_template('consoles.html', consoles = consoles)




    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Simples formulário de login. Em POST valida um par hard-coded e retorna uma mensagem."""
        message = ''
        if request.method == 'POST':
            username = request.form.get('username', '')
            password = request.form.get('password', '')
            # validação simples hard-coded (exemplo)
            if username == 'admin' and password == 'secret':
                message = f'Bem-vindo, {username}!'
            else:
                message = 'Usuário ou senha inválidos.'
        return render_template('login.html', message=message)
    
    
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            listaGames.append({'titulo' : request.form.get('titulo'), 'ano' : request.form.get('ano'), 'categoria' : request.form.get('categoria')})
            return redirect(url_for('cadgames'))
        return render_template('cadgames.html',
                               listaGames = listaGames)