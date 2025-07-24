{{ config(
    materialized='table',
    schema='metrics',
    alias='metrics',
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
    SUM(CASE 
        WHEN p.units_in_stock < p.reorder_level THEN 1 
        ELSE 0 
    END) AS low_stock_products,
    -- Produtos com alto estoque
    SUM(CASE 
        WHEN p.units_in_stock > p.reorder_level * 2 THEN 1 
        ELSE 0 
    END) AS high_stock_products,
    -- Produtos que precisam de reabastecimento frequente por região
    SUM(CASE 
        WHEN p.units_in_stock < p.reorder_level AND c.country IS NOT NULL 
        THEN 1 
        ELSE 0 
    END) AS frequent_restock_products_by_region,
    -- Produtos que precisam de reabastecimento frequente por fornecedor
    s.supplier_id,
    s.company_name AS supplier_name,
    SUM(CASE 
        WHEN p.units_in_stock < p.reorder_level THEN 1 
        ELSE 0 
    END) AS frequent_restock_products_by_supplier,
    -- Produtos descontinuados com vendas
    SUM(CASE 
        WHEN p.discontinued = 1 
        THEN 1 
        ELSE 0 
    END) AS discontinued_products_with_sales,
    -- Margem de lucro por produto
    AVG((od.unit_price * od.quantity * (1 - od.discount)) / od.quantity - p.unit_price) * AVG(od.quantity) AS avg_profit_per_product,
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
            SELECT MAX(o2.order_date::date) 
            FROM public.orders o2 
            JOIN public.order_details od2 ON o2.order_id = od2.order_id 
            WHERE o2.customer_id = c.customer_id
        ) >= (SELECT MAX(o3.order_date::date) FROM public.orders o3 JOIN public.order_details od3 ON o3.order_id = od3.order_id) - INTERVAL '6 months'
        THEN 'Ativo'
        ELSE 'Inativo'
    END AS customer_status
FROM public.orders o
JOIN public.order_details od ON o.order_id = od.order_id
JOIN public.customers c ON o.customer_id = c.customer_id
JOIN public.products p ON od.product_id = p.product_id
JOIN public.categories cat ON p.category_id = cat.category_id
JOIN public.suppliers s ON p.supplier_id = s.supplier_id
JOIN public.shippers sh ON o.ship_via = sh.shipper_id
JOIN public.employees e ON o.employee_id = e.employee_id
JOIN public.employee_territories et ON e.employee_id = et.employee_id
JOIN public.territories t ON et.territory_id = t.territory_id
JOIN public.region r ON t.region_id = r.region_id
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