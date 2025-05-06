
# GCP Data Pipeline Project

## ✅ Project Overview
This project demonstrates a modern data engineering pipeline that transfers data from local sources (PostgreSQL and flat files) to Google Cloud Platform (GCS and BigQuery), using Terraform for infrastructure 
provisioning, Airflow for orchestration, dbt for transformations, and Looker for analytics.

---

## 📁 Folder Structure
```
.
├── airflow/                # Airflow DAGs and config (non-Dockerized)
├── data/                   # Local files (e.g., CSVs)
├── dbt/                    # dbt models and config
├── terraform/              # Infrastructure-as-code scripts
├── scripts/                # Python scripts for data movement
├── README.md               # Project documentation
```

---

## 🔧 Tools & Technologies
- **PostgreSQL** – Source relational database  
- **Python SDK (google-cloud-storage, bigquery)** – For uploading and querying  
- **Google Cloud Storage (GCS)** – File storage layer  
- **BigQuery** – Data warehouse  
- **Terraform** – Infrastructure provisioning  
- **Apache Airflow** – Workflow orchestration  
- **dbt** – Data transformation  
- **Looker** – Data visualization  


---

## 🚀 Pipeline Overview
1. **Provision Infrastructure**  
   Using Terraform to create:
   - GCS bucket
   - BigQuery dataset
   - GCP VM instance for Airflow

2. **Ingest Data**
   - Extract data from PostgreSQL and flat files (e.g., CSV).
   - Load data into GCS using Python scripts.

3. **Load into BigQuery**
   - Transfer staged data from GCS to BigQuery using Python SDK.

4. **Transform with dbt**
   - Run dbt models inside the Airflow DAG to apply transformations in BigQuery.

5. **Visualize with Looker**
   - Build dashboards and visualizations using modeled data in BigQuery.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure GCP Credentials  
Set your service account key:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/key.json"
```

### 4. Deploy Infrastructure
```bash
cd terraform
terraform init
terraform apply
```

### 5. Run Airflow  
Ensure Airflow is installed and configured to run DAGs manually on your VM or local machine.

---

## 🛠 DAGs & Scripts
- `load_to_gcs.py` – Uploads data from local sources to GCS  
- `load_to_bigquery.py` – Loads data from GCS into BigQuery  
- `transform_with_dbt.py` – Triggers dbt transformations  
- Airflow DAG `gcp_data_pipeline.py` orchestrates the entire process

---

## 📊 Visualization
Once data is in BigQuery and transformed, connect Looker to your BigQuery dataset and build reports from the dbt models.

---

## 📌 Notes
- Ensure proper IAM permissions are set for GCP services.  
- Secrets should be managed securely (e.g., via Airflow Variables or Secret Manager).  

