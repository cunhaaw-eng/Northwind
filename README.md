# Desafio - Northwind Traders

## Visão Geral
O projeto Northwind Traders é uma solução de análise de dados desenvolvida para fornecer insights de negócios a partir do banco de dados Northwind, utilizando modelagem dimensional. Ele utiliza **dbt** para transformação de dados, **PostgreSQL** como banco de dados e **Streamlit** para visualização. O projeto calcula métricas-chave, como ticket médio, churn de clientes, receita por região/categoria/funcionário, tempo de entrega e status de estoque, apoiando decisões estratégicas para uma empresa em crescimento.

## Objetivos do Projeto
- Consolidar dados do Northwind em dimensões e fatos para análises eficientes.
- Calcular métricas como ticket médio, taxas de churn, receita, tempo de entrega e status de estoque.

## Para rodar o projeto:

1. Vá até a pasta `Northwind`.
2. Ative o ambiente virtual:
   - **Windows:** `venv/Scripts/Activate`
   - **Linux:** `source venv/bin/activate`
3. Com o ambiente ativado, instale as dependências:
   ```bash
   pip install -r requirements.txt

 ```bash
northwind_dbt:
dbt run
para ver a documentação do projeto>
dbt generate docs
dbt docs serve

para carregar o dashboard
 ```bash
scripts > streamlit run ./bi_northwind.py

Qualquer dúvidas, enviar para: cunhaa.mcss@gmail.com
