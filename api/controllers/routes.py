from flask import render_template, request
import urllib.request
import json

URL_FRANKFURTER = 'https://api.frankfurter.dev/v2'

def init_app(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/apimoedas', methods=['GET'])
    def apimoedas():
        try:
            urlAPI = f'{URL_FRANKFURTER}/currencies'
            req = urllib.request.Request(
            )
            resposta = urllib.request.urlopen(req)
            dados = json.loads(resposta.read())

            # Pega todos os códigos disponíveis na API
            codigos_disponiveis = [m['iso_code'] for m in dados]

            # Filtra só as que existem na API
            moedas_desejadas = ['BRL', 'USD', 'EUR', 'GBP', 'ARS', 'CLP', 'COP', 'MXN']
            
            moedas = []
            for m in dados:
                if m['iso_code'] in moedas_desejadas:
                    moedas.append({
                        'codigo': m['iso_code'],
                        'nome': m['name'],
                        'simbolo': m['symbol']
                    })
            moedas.sort(key=lambda x: moedas_desejadas.index(x['codigo']))

        except Exception:
            # Fallback
            moedas = [
                {"codigo": "BRL", "nome": "Real brasileiro", "simbolo": "R$"},
                {"codigo": "USD", "nome": "Dólar americano", "simbolo": "US$"},
                {"codigo": "EUR", "nome": "Euro", "simbolo": "€"},
                {"codigo": "GBP", "nome": "Libra esterlina", "simbolo": "£"},
                {"codigo": "ARS", "nome": "Peso argentino", "simbolo": "ARS$"},
                {"codigo": "CLP", "nome": "Peso chileno", "simbolo": "CLP$"},
                {"codigo": "COP", "nome": "Peso colombiano", "simbolo": "COP$"},
                {"codigo": "MXN", "nome": "Peso mexicano", "simbolo": "MX$"}
            ]

        resultado = None
        erro = None

        base = request.args.get('base')
        quotes = request.args.get('quotes')
        amount = request.args.get('amount', '1')

        if base and quotes:
            # Validação: não pode ser a mesma moeda
            if base == quotes:
                erro = "A moeda base e a moeda de comparação não podem ser a mesma. Escolha moedas diferentes."
            else:
                try:
                    # Endpoint correto da v2: /v2/rates?base=XXX&quotes=YYY
                    url_cotacao = f'{URL_FRANKFURTER}/rates?base={base}&quotes={quotes}'
                    
                    req = urllib.request.Request(
                        url_cotacao,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                    )
                    resposta = urllib.request.urlopen(req)
                    dados_cotacao = json.loads(resposta.read())

                    comparacoes = []
                    for item in dados_cotacao:
                        codigo = item['quote']
                        taxa = item['rate']
                        data = item['date']
                        
                        # Busca nome da moeda
                        nome_moeda = next((m['nome'] for m in moedas if m['codigo'] == codigo), codigo)
                        
                        valor = float(amount)
                        convertido = valor * taxa
                        
                        comparacoes.append({
                            'codigo': codigo,
                            'nome': nome_moeda,
                            'taxa': taxa,
                            'taxa_formatada': f"{taxa:,.4f}",
                            'valor_original': valor,
                            'valor_formatado': f"{valor:,.2f} {base}",
                            'convertido': f"{convertido:,.2f} {codigo}"
                        })

                    base_nome = next((m['nome'] for m in moedas if m['codigo'] == base), base)

                    resultado = {
                        'base': base,
                        'base_nome': base_nome,
                        'data': data,
                        'comparacoes': comparacoes
                    }

                except urllib.error.HTTPError as e:
                    if e.code == 404:
                        erro = "Moeda não encontrada na API. A Frankfurter v2 pode não suportar essa moeda (ex: ARS, CLP, COP). Tente USD, EUR, GBP, BRL ou MXN."
                    elif e.code == 403:
                        erro = "Acesso negado pela API. Tente novamente mais tarde."
                    elif e.code == 422:
                        body = e.read().decode()
                        erro = f"Requisição inválida: {body}"
                    else:
                        erro = f"Erro HTTP {e.code}: {e.reason}"
                except Exception as e:
                    erro = f"Erro ao buscar cotação: {str(e)}"

        return render_template('apimoedas.html', 
                               moedas=moedas, 
                               resultado=resultado, 
                               erro=erro,
                               base_selecionada=base,
                               quote_selecionada=quotes,
                               amount_valor=amount)