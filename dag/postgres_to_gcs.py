import pandas as pd
import psycopg2
import os
from google.cloud import storage
import tempfile

# PostgreSQL connection configuration
POSTGRES_CONFIG = {
    "host": "7.tcp.eu.ngrok.io",
    "database": "apex_db",
    "user": "postgres",
    "password": "OYE080tayo@",
    "port": 19309
}

# GCP bucket name
BUCKET_NAME = "onpremtocloud-raw-data"

def upload_to_gcs(bucket_name, source_file_path, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    print(f"✅ Uploaded {source_file_path} to gs://{bucket_name}/{destination_blob_name}")

def upload_postgres_tables_to_gcs():
    try:
        print("🔄 Connecting to PostgreSQL...")
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        tables = [row[0] for row in cur.fetchall()]
        print(f"📋 Found tables: {tables}")

        for table in tables:
            csv_file = f"{table}.csv"
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(query, conn)
            
            # Save CSV to temporary location
            temp_file = f"/tmp/{csv_file}"  # Or use tempfile
            df.to_csv(temp_file, index=False)
            
            # Upload to GCS
            upload_to_gcs(BUCKET_NAME, temp_file, f"raw/files/{csv_file}")
            
            # Clean up local CSV file after upload
            os.remove(temp_file)

    except Exception as e:
        print(f"⚠️ Error: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    upload_postgres_tables_to_gcs()





