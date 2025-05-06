from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.operators.bash import BashOperator
import sys

sys.path.append('/home/oyetayoadedamola/dag')

from postgres_to_gcs import upload_postgres_tables_to_gcs
from local_files_to_gcs import upload_local_files_to_gcs
from gcs_to_bigquery import load_data_from_gcs_to_bigquery

# -------------------------------------
# DAG CONFIG
# -------------------------------------
BUCKET_NAME = "onpremtocloud-raw-data"
BQ_DATASET = "analytics_dataset"  # 🔁 Replace with your actual dataset

default_args = {
    'start_date': datetime(2025, 4, 14),
    'retries': 1
}

with DAG(
    dag_id='postgres_local_to_bigquery_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Extracts data from Postgres + local CSVs, uploads to GCS, then loads into BigQuery.',
) as dag:

    # Task 1: Upload PostgreSQL tables to GCS
    upload_postgres_task = PythonOperator(
        task_id='upload_postgres_to_gcs',
        python_callable=upload_postgres_tables_to_gcs,
        op_kwargs={"bucket_name": BUCKET_NAME}
    )

    # Task 2: Upload local files to GCS
    upload_local_files_task = PythonOperator(
        task_id='upload_local_files_to_gcs',
        python_callable=upload_local_files_to_gcs,
        op_kwargs={"bucket_name": BUCKET_NAME}
    )

    # Task 3: Load from GCS to BigQuery
    load_bigquery_task = PythonOperator(
        task_id='load_gcs_to_bigquery',
        python_callable=load_data_from_gcs_to_bigquery,
        op_kwargs={
            "bucket_name": BUCKET_NAME,
            "dataset_name": BQ_DATASET
        } 
    )

    # Task 4a: Run second dbt merge model
    nigeria_customer_transform = BashOperator(
        task_id='run_dbt_merge_nigeria_customers',
        bash_command='cd /home/oyetayoadedamola/dbt_transformation && dbt run --select stg_nigeria_customers'
    )

    # Task 4b: Run second dbt merge model
    kenya_customer_transform = BashOperator(
        task_id='run_dbt_merge_kenya_transactions',
        bash_command='cd /home/oyetayoadedamola/dbt_transformation && dbt run --select stg_kenya_customers'
    )

    # Task 4c: Run second dbt merge model
    ghana_customer_transform = BashOperator(
        task_id='run_dbt_merge_ghana_transactions',
        bash_command='cd /home/oyetayoadedamola/dbt_transformation && dbt run --select stg_ghana_customers'
   )

   # Task 5a: Run second dbt merge model
    run_dbt_merge_customer = BashOperator(
        task_id='run_dbt_merge_customers',
        bash_command='cd /home/oyetayoadedamola/dbt_transformation && dbt run --select merged_customer_model'
    )

    # Task 5b: Run second dbt merge model
    run_dbt_merge_transaction = BashOperator(
        task_id='run_dbt_merge_transactions',
        bash_command='cd /home/oyetayoadedamola/dbt_transformation && dbt run --select merged_transaction_model'
    )


    # Task sequence
    [upload_postgres_task, upload_local_files_task] >> load_bigquery_task >> [nigeria_customer_transform, kenya_customer_transform, ghana_customer_transform] >> run_dbt_merge_transaction >> run_dbt_merge_customer

