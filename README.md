# Desafio Dados

Bem vindo(a)! Essa é a minha resolução do desafio proposto.

## Ferramentas Utilizadas

- Para extração dos dados e geração das métricas foi utilizada a linguagem de programação Python juntamente com sua biblioteca de tratamento de dados Pandas;
- Para a visualização e plotagem dos gráficos foi utilizado o framework Dash e a biblioteca Plotly.

## Cenário

Uma empresa do mercado financeiro precisa visualizar os informes diários dos fundos de investimento do mercado. A CVM disponibiliza planilhas com os informes de cada mês do último ano na url http://dados.cvm.gov.br/dataset/fi-doc-inf_diario.

### Primeira Etapa

- Carregamento das tabelas contidas nos arquivos;
- Criação de uma lista com todas as tabelas carregadas;
- Concatenação de todas as tabelas para criação de apenas uma grande tabela que chamaremos de base de dados.

### Segunda Etapa

A partir da base de dados é criada uma dashboard com três gráficos com o crescimento das seguintes informações de um determinado fundo:

- Valor Patrimonial Líquido
- Valor Cota
- Rendimento => calculado a partir do valor patrimonial líquido do dia interior.

### Terceira Etapa

Criação dos Filtros:

- Seleção do fundo desejado (através do CNPJ);
- Seleção do gráfico (Crescimento do Valor Patrimonial Líquido, Valor Cota ou Rendimento)

## Considerações

- Para rodar, copie o arquivo [metricas-e-exibicao.py](http://metricas-e-exibicao.py/)
- Verifique se todas as bibliotecas e frameworks estão instalados em seu ambiente de execução.
- O dash será gerado, por padrão, na porta TCP 8050, que pode ser acessada em [http://localhost:8050/](http://localhost:8050/).
