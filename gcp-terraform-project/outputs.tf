output "bucket_name" {
  description = "Name of the GCS bucket"
  value       = google_storage_bucket.raw_data.name
}

output "bq_dataset" {
  description = "ID of the BigQuery dataset"
  value       = google_bigquery_dataset.analytics.dataset_id
}

output "vm_ip" {
  description = "External IP of the Airflow VM"
  value       = google_compute_instance.airflow_vm.network_interface[0].access_config[0].nat_ip
}
