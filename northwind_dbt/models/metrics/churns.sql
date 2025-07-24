{{ config(
    materialized='table',
    schema='metrics',
    alias='churns',
    tags=['churns']
) }}

SELECT
    -- Churn 6 meses
    COUNT(DISTINCT CASE 
        WHEN (
            SELECT MAX(o2.order_date::date)
            FROM public.orders o2
            JOIN public.order_details od2 ON o2.order_id = od2.order_id
            WHERE o2.customer_id = c.customer_id
        ) < (SELECT MAX(o3.order_date::date) FROM public.orders o3 JOIN public.order_details od3 ON o3.order_id = od3.order_id) - INTERVAL '6 months'
        THEN c.customer_id
    END) * 100.0 / NULLIF(COUNT(DISTINCT c.customer_id), 0) AS churn_rate_6m,
    -- Churn 12 meses
    COUNT(DISTINCT CASE 
        WHEN (
            SELECT MAX(o2.order_date::date)
            FROM public.orders o2
            JOIN public.order_details od2 ON o2.order_id = od2.order_id
            WHERE o2.customer_id = c.customer_id
        ) < (SELECT MAX(o3.order_date::date) FROM public.orders o3 JOIN public.order_details od3 ON o3.order_id = od3.order_id) - INTERVAL '12 months'
        THEN c.customer_id
    END) * 100.0 / NULLIF(COUNT(DISTINCT c.customer_id), 0) AS churn_rate_12m
FROM public.customers c