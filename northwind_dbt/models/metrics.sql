{{ config(
    materialized='table',
    alias='metrics',
    schema='metrics',
    tags=['metrics']
) }}

SELECT 
    -- Ticket Médio por Pedido
    AVG(od.unit_price * od.quantity * (1 - od.discount)) AS avg_ticket_per_order,

    -- Ticket Médio por Cliente
    SUM(od.unit_price * od.quantity * (1 - od.discount)) / NULLIF(COUNT(DISTINCT o.customer_id), 0) AS avg_ticket_per_customer,

    -- Ticket Médio por Região
    c.country AS region,
    AVG(od.unit_price * od.quantity * (1 - od.discount)) AS avg_ticket_per_region,

    -- Churn 6 meses
    COUNT(DISTINCT CASE 
        WHEN (
            SELECT MAX(TO_DATE(o2.order_date, 'YYYY-MM-DD'))
            FROM orders o2
            WHERE o2.customer_id = c.customer_id 
              AND o2.order_date <> '0000-00-00'
        ) < CURRENT_DATE - INTERVAL '6 months'
        THEN c.customer_id
    END) * 100.0 / NULLIF(COUNT(DISTINCT c.customer_id), 0) AS churn_rate_6m,

    -- Churn 12 meses
    COUNT(DISTINCT CASE 
        WHEN (
            SELECT MAX(TO_DATE(o2.order_date, 'YYYY-MM-DD'))
            FROM orders o2
            WHERE o2.customer_id = c.customer_id 
              AND o2.order_date <> '0000-00-00'
        ) < CURRENT_DATE - INTERVAL '12 months'
        THEN c.customer_id
    END) * 100.0 / NULLIF(COUNT(DISTINCT c.customer_id), 0) AS churn_rate_12m,

    -- Receita por País
    SUM(od.unit_price * od.quantity * (1 - od.discount)) AS revenue_by_country,

    -- Receita por Categoria
    cat.category_name,
    SUM(od.unit_price * od.quantity * (1 - od.discount)) AS revenue_by_category,

    -- Receita por Funcionário
    e.employee_id,
    e.first_name || ' ' || e.last_name AS employee_name,
    SUM(od.unit_price * od.quantity * (1 - od.discount)) AS revenue_by_employee,

    -- Tempo Médio de Entrega
    AVG(CASE 
        WHEN o.shipped_date IS NOT NULL AND o.order_date IS NOT NULL 
        THEN o.shipped_date::date - o.order_date::date 
    END) AS avg_delivery_time_days,

    -- Produtos mais vendidos
    p.product_id,
    p.product_name,
    SUM(od.quantity) AS quantity_sold,

    -- Região com mais compras
    c.country AS top_revenue_region,
    SUM(od.unit_price * od.quantity * (1 - od.discount)) AS total_revenue_by_region,

    -- Total de funcionários por região
    r.region_description,
    COUNT(DISTINCT e.employee_id) AS total_employees_by_region,

    -- Produtos com baixo estoque
    COUNT(DISTINCT CASE WHEN p.units_in_stock < p.reorder_level THEN p.product_id END) AS low_stock_products,

    -- Produtos com alto estoque
    COUNT(DISTINCT CASE WHEN p.units_in_stock > 2 * p.reorder_level THEN p.product_id END) AS high_stock_products,

    -- Produtos que precisam de reabastecimento frequente por região
    COUNT(DISTINCT CASE 
        WHEN p.units_in_stock < p.reorder_level 
        AND c.country IS NOT NULL 
        THEN p.product_id 
    END) AS frequent_restock_products_by_region,

    -- Produtos que precisam de reabastecimento frequente por fornecedor
    s.supplier_id,
    s.company_name AS supplier_name,
    COUNT(DISTINCT CASE 
        WHEN p.units_in_stock < p.reorder_level 
        THEN p.product_id 
    END) AS frequent_restock_products_by_supplier,

    -- Produtos descontinuados com vendas
    COUNT(DISTINCT CASE 
        WHEN p.discontinued = 1 
        THEN p.product_id 
    END) AS discontinued_products_with_sales,

    -- Margem de lucro por produto (estimativa)
    AVG(od.unit_price - p.unit_price) * AVG(od.quantity) AS avg_profit_per_product,

    -- Volume de pedidos por transportadora
    sh.shipper_id,
    sh.company_name AS shipper_name,
    COUNT(DISTINCT o.order_id) AS total_orders_by_shipper,

    -- Custo médio de frete por transportadora
    AVG(o.freight) AS avg_freight_cost_by_shipper,

    -- Status do cliente
    c.customer_id,
    c.company_name AS customer_name,
    CASE 
        WHEN (
            SELECT MAX(TO_DATE(o2.order_date, 'YYYY-MM-DD'))
            FROM orders o2
            WHERE o2.customer_id = c.customer_id
              AND o2.order_date <> '0000-00-00'
        ) >= CURRENT_DATE - INTERVAL '6 months'
        THEN 'Ativo'
        ELSE 'Inativo'
    END AS customer_status

FROM orders o
JOIN order_details od ON o.order_id = od.order_id
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON od.product_id = p.product_id
JOIN categories cat ON p.category_id = cat.category_id
JOIN suppliers s ON p.supplier_id = s.supplier_id
JOIN shippers sh ON o.ship_via = sh.shipper_id
JOIN employees e ON o.employee_id = e.employee_id
JOIN employee_territories et ON e.employee_id = et.employee_id
JOIN territories t ON et.territory_id = t.territory_id
JOIN region r ON t.region_id = r.region_id

GROUP BY 
    c.country,
    cat.category_name,
    e.employee_id,
    e.first_name,
    e.last_name,
    p.product_id,
    p.product_name,
    s.supplier_id,
    s.company_name,
    sh.shipper_id,
    sh.company_name,
    r.region_description,
    c.customer_id,
    c.company_name
