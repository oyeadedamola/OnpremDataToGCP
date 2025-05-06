from google.cloud import storage

# GCP bucket name
BUCKET_NAME = "onpremtocloud-raw-data"

# Local files to upload
ADDITIONAL_FILES = [
    {"local_path": "home/oyetayoadedamola/data_storage/products.csv", "gcs_path": "raw/files/products.csv"},
    {"local_path": "home/oyetayoadedamola/data_storage/regions.csv", "gcs_path": "raw/files/regions.csv"}
]

def upload_to_gcs(bucket_name, source_file_path, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    print(f"✅ Uploaded {source_file_path} to gs://{bucket_name}/{destination_blob_name}")

def upload_local_files_to_gcs():
    for file in ADDITIONAL_FILES:
        upload_to_gcs(BUCKET_NAME, file["local_path"], file["gcs_path"])

if __name__ == "__main__":
    upload_local_files_to_gcs()
