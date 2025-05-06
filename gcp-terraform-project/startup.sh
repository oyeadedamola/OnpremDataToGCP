#!/bin/bash

# Log output for debugging
exec > /var/log/startup-script.log 2>&1
set -e

echo "🔧 Updating system..."
apt-get update && apt-get upgrade -y

echo "🐍 Installing Python 3 and pip..."
apt-get install -y python3 python3-pip python3-venv

echo "🔧 Installing system dependencies..."
apt-get install -y build-essential libssl-dev libffi-dev libpq-dev git

echo "📦 Creating Airflow virtual environment..."
python3 -m venv /opt/airflow_venv
source /opt/airflow_venv/bin/activate

echo "🌬️ Installing Apache Airflow..."
AIRFLOW_VERSION=2.8.1
PYTHON_VERSION="$(python3 --version | cut -d ' ' -f2 | cut -d '.' -f1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install --upgrade pip setuptools wheel
pip install apache-airflow==${AIRFLOW_VERSION} --constraint "${CONSTRAINT_URL}"

echo "📁 Setting up Airflow folders..."
mkdir -p /opt/airflow/{dags,logs,plugins}
export AIRFLOW_HOME=/opt/airflow

echo "🌬️ Initializing Airflow..."
airflow db init
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin

# Optional: Launch Airflow webserver and scheduler in background
echo "🚀 Starting Airflow services..."
airflow webserver -p 8080 &  # Web UI
airflow scheduler &          # DAG scheduler

echo "⚙️ Installing dbt + BigQuery adapter..."
pip install dbt-core dbt-bigquery

echo "☁️ Installing Google Cloud SDK..."
apt-get install -y apt-transport-https ca-certificates gnupg curl
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
apt-get update && apt-get install -y google-cloud-sdk

echo "✅ Setup complete!"
