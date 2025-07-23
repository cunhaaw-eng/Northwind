# Projeto de Análise de Dados Northwind Traders

## Visão Geral
O projeto Northwind Traders é uma solução de análise de dados desenvolvida para fornecer insights de negócios a partir do banco de dados Northwind, utilizando modelagem dimensional. Ele utiliza **dbt** para transformação de dados, **PostgreSQL** como banco de dados e **PowerBI** para visualização. O projeto calcula métricas-chave, como ticket médio, churn de clientes, receita por região/categoria/funcionário, tempo de entrega e status de estoque, apoiando decisões estratégicas para uma empresa em crescimento.

## Objetivos do Projeto
- Consolidar dados do Northwind em dimensões e fatos para análises eficientes.
- Calcular métricas como ticket médio, taxas de churn, receita, tempo de entrega e status de estoque.
- Disponibilizar relatórios interativos no PowerBI Desktop e PowerBI Service.
- Garantir escalabilidade e controle de acesso para uma equipe em expansão (de 30 funcionários para estruturas maiores).

## Estrutura do Projeto
```plaintext
northwind_indicium/
├── scripts/
│   └── load_data.py
├── northwind_dbt/
│   ├── models/
│   │   ├── dimensions/
│   │   │   ├── d_customer.sql
│   │   │   ├── d_product.sql
│   │   │   ├── d_calendar.sql
│   │   │   ├── d_category.sql
│   │   │   ├── d_supplier.sql
│   │   │   ├── d_shipper.sql
│   │   │   ├── d_employee.sql
│   │   │   ├── d_region.sql
│   │   ├── facts/
│   │   │   ├── f_sales.sql
│   │   │   ├── f_inventory.sql
│   │   ├── metrics/
│   │   │   ├── metrics.sql
│   ├── profiles.yml
│   ├── dbt_project.yml
├── reports/
│   └── northwind_metrics.pbix
├── docs/
│   └── northwind_project_documentation.docx
