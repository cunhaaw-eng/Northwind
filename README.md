# Projeto de Análise de Dados Northwind Traders

## Visão Geral
O projeto Northwind Traders é uma solução de análise de dados desenvolvida para fornecer insights de negócios a partir do banco de dados Northwind, utilizando modelagem dimensional. Ele utiliza **dbt** para transformação de dados, **PostgreSQL** como banco de dados e **Streamlit** para visualização. O projeto calcula métricas-chave, como ticket médio, churn de clientes, receita por região/categoria/funcionário, tempo de entrega e status de estoque, apoiando decisões estratégicas para uma empresa em crescimento.

## Objetivos do Projeto
- Consolidar dados do Northwind em dimensões e fatos para análises eficientes.
- Calcular métricas como ticket médio, taxas de churn, receita, tempo de entrega e status de estoque.

#Para rodar o projeto: 
- vá a pasta Northwind
- em Windows: execute venv/Scripts/Activate ou em Linux source venv/bin/activate

northwind_dbt:
dbt run
para ver a documentação do projeto>
dbt generate docs
dbt docs serve

para carregar o dash
scripts > streamlit run ./bi_northwind.py
