{{ config(
    materialized='table',
    alias='merged_transaction'
) }}

{% set pattern = 'transaction' %}  {# will match any table with 'transaction' in the name #}

{% set matching_tables_query %}
    SELECT table_name
    FROM `{{ target.project }}.{{ target.schema }}.INFORMATION_SCHEMA.TABLES`
    WHERE table_name LIKE '%{{ pattern }}%'
{% endset %}

{% set results = run_query(matching_tables_query) %}

{% if execute %}
    {% set table_names = results.columns[0].values() %}
{% endif %}

{% if not execute %}
    SELECT 'This is a dry run.'
{% elif table_names | length == 0 %}
    {{ exceptions.raise_compiler_error("No tables matched the pattern '%" ~ pattern ~ "%'") }}
{% else %}
    {% for table in table_names %}
        SELECT * FROM `{{ target.project }}.{{ target.schema }}.{{ table }}`
        {% if not loop.last %}
            UNION ALL
        {% endif %}
    {% endfor %}
{% endif %}
