terraform {
  required_version = ">= 1.2.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# -------------------------
# GCS Bucket for Raw Data
# -------------------------
resource "google_storage_bucket" "raw_data" {
  name     = "${var.project_id}-raw-data"
  location = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}

# -------------------------
# BigQuery Dataset
# -------------------------
resource "google_bigquery_dataset" "analytics" {
  dataset_id                  = "analytics_dataset"
  location                    = var.region
  delete_contents_on_destroy = true
}

# -------------------------
# Service Account for Airflow/dbt
# -------------------------
resource "google_service_account" "pipeline_sa" {
  account_id   = "data-pipeline-sa"
  display_name = "Data Pipeline Service Account"
}

resource "google_project_iam_member" "sa_storage_access" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

resource "google_project_iam_member" "sa_bigquery_access" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

# -------------------------
# Google Compute Engine (Airflow VM)
# -------------------------
resource "google_compute_instance" "airflow_vm" {
  name         = "airflow-vm"
  machine_type = "e2-medium"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network       = "default"
    access_config {}
  }

  service_account {
    email  = google_service_account.pipeline_sa.email
    scopes = ["cloud-platform"]
  }

  metadata_startup_script = file("startup.sh")
}
