# importando bibliotecas que serão utilizadas
import datetime
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from dash.dcc import Graph, Dropdown


# funcao cálculo do rendimento
def calculo_rendimento(patrimonio_liquido_atual, patrimonio_liquido_anterior):
    rendimento = ((patrimonio_liquido_atual / patrimonio_liquido_anterior) - 1) * 100
    return rendimento


# funcao que faz a leitura e extração das tabelas do último ano
def lendo_arquivos(ano_inicio, mes_inicio, ano_fim, mes_fim):
    # criando uma lista com todas as tabelas .csv
    tabelas = []

    # lendo tabelas do ano inicial a partir do mês incial e inserindo na lista "tabelas".
    for mes in range(mes_inicio, 13):
        if mes < 10:
            url_base = f'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano_inicio}0{mes}.zip'
        else:
            url_base = f'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano_inicio}{mes}.zip'
        df = pd.read_csv(url_base, sep=';')
        tabelas.append(df)

    # lendo tabelas do ano final até o mes final e inserindo na lista "tabelas".
    for mes in range(1, mes_fim + 1):
        if mes < 10:
            url_base = f'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano_fim}0{mes}.zip'
        else:
            url_base = f'http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano_fim}{mes}.zip'
        df = pd.read_csv(url_base, sep=';')
        tabelas.append(df)
    return tabelas


# definindo parâmetros (os dados sempre serão referentes ao último ano)
ano_inicial = datetime.datetime.now().year - 1  # ano inicial do intervalo
mes_inicial = datetime.datetime.now().month  # mês inicial do intervalo
ano_final = datetime.datetime.now().year  # ano final do intervalo
mes_final = datetime.datetime.now().month  # mês final do intervalo

# chamando funcao de leitura
data_frames = lendo_arquivos(ano_inicial, mes_inicial, ano_final, mes_final)

# concatenando todas as tabelas lidas, ajustando o index e verificando a integridade dos dados para criar a nossa base de dados
base_de_dados = pd.concat(data_frames, verify_integrity=True, ignore_index=True)

# ____________________________________________________________________________________

# Métricas e exibição utilizando as bibliotecas Plotly e Dash
app = Dash(__name__)
# Estruturando o meu dashboard com uma árvore html.
app.layout = html.Div(html.Div([
    html.H1('INFORMES DIÁRIOS - FUNDOS DE INVESTIMENTO'),
    html.H3('Fonte: http://dados.cvm.gov.br/dataset/fi-doc-inf_diario'),
    html.H2('Selecione um FI (CNPJ) e o tipo de gráfico desejado:'),
    # criando os dois dropdowns que serão utilizados como filtro.
    html.H2(children=[dcc.Dropdown(
        base_de_dados['CNPJ_FUNDO'].unique(),
        value='00.068.305/0001-35',
        id='filter1_dropdown'
    ), Dropdown(
        options=[
            {'label': 'Cota', 'value': 'VL_QUOTA'},
            {'label': 'Patrimônio Líquido', 'value': 'VL_PATRIM_LIQ'},
            {'label': 'Rendimento', 'value': 'RENDIMENTO'}
        ],
        value='VL_QUOTA',
        id='filter2_dropdown'),
        # Criando gráfico que será retornado de acordo com os filtros
        Graph(id="graph")
    ])
])
)


# criando função callback que será utilizada para atualizar nosso gráfico de forma interativa
# gráfico como valor de saída
# filtros como valores de entrada
@app.callback(
    Output("graph", "figure"),
    [Input("filter1_dropdown", "value"),
     Input("filter2_dropdown", "value")])
def update_graph(value, filter2_dropdown):
    # função que calcula as métricas e atualiza os gráficos de acordo com a interação
    base_filtrada = base_de_dados.query(f'CNPJ_FUNDO == "{value}"')
    if filter2_dropdown == 'RENDIMENTO':
        # lista com os valores de patrimônio líquido
        patrimonio_liquido = base_filtrada['VL_PATRIM_LIQ'].array
        # lista que será incrementada com os valores de rendimento calculados
        # o primeiro elemento é 0 pois não temos "dia anterior" ao inicial.
        lista_rendimentos = [0]
        for c in range(0, len(patrimonio_liquido) - 1):
            patrimonio_liquido_anterior = patrimonio_liquido[c]
            patrimonio_liquido_atual = patrimonio_liquido[c + 1]
            # cálculo rendimento
            rendimento = calculo_rendimento(patrimonio_liquido_atual, patrimonio_liquido_anterior)
            lista_rendimentos.append(rendimento)

        datas = base_filtrada['DT_COMPTC'].array
        # plotando gráfico de rendimento
        fig = px.line(
            x=datas, y=lista_rendimentos,
            title="Série Histórica", height=500, labels={
                'x': 'DATA', 'y': 'RENDIMENTO EM RELAÇÃO AO DIA ANTERIOR (%)'
            }
        )

    else:
        # plotando gráfico com a séria histórica (ou valor da cota ou patrimônio líquido)
        fig = px.line(
            x=base_filtrada['DT_COMPTC'], y=base_filtrada[f'{filter2_dropdown}'],
            title="Série Histórica", height=500, labels={
                'x': 'DATA', 'y': f'{filter2_dropdown}'
            }
        )
    return fig


# iniciando o servidor local.
app.run_server(debug=True)
