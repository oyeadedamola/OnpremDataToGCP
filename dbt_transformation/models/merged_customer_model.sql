{{ config(
    materialized='table',
    alias='customer_table'
) }}

SELECT * FROM {{ ref('stg_kenya_customers') }}
UNION ALL
SELECT * FROM {{ ref('stg_ghana_customers') }}
UNION ALL
SELECT * FROM {{ ref('stg_nigeria_customers') }}
