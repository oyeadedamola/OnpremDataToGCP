import os
import logging
from google.cloud import bigquery
from google.cloud import storage
from google.api_core.exceptions import GoogleAPIError

def load_data_from_gcs_to_bigquery(bucket_name, dataset_name):
    logger = logging.getLogger("airflow.task")

    storage_client = storage.Client()
    bq_client = bigquery.Client()

    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix='raw/')  # Adjust this prefix as needed

    for blob in blobs:
        if not blob.name.endswith(".csv"):
            continue

        file_name = os.path.basename(blob.name)
        table_name = os.path.splitext(file_name)[0]
        table_id = f"{bq_client.project}.{dataset_name}.{table_name}"
        gcs_uri = f"gs://{bucket_name}/{blob.name}"

        logger.info(f"🔄 Loading {gcs_uri} into {table_id}...")

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        try:
            load_job = bq_client.load_table_from_uri(
                gcs_uri,
                table_id,
                job_config=job_config
            )
            load_job.result()  # Wait for completion
            logger.info(f"✅ Loaded {gcs_uri} into {table_id}")

        except GoogleAPIError as e:
            logger.error(f"❌ Failed to load {gcs_uri} to {table_id}: {e}")
        except Exception as e:
            logger.exception(f"❌ Unexpected error loading {gcs_uri}: {e}")




