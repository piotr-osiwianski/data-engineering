#!/bin/bash
# Script: start_env.sh
# Purpose: Start Airflow Webserver or Scheduler with required environment variables

cd "$(dirname "$0")"
source venv/bin/activate
export AIRFLOW_HOME=$(pwd)/airflow_home
export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/dags
export AIRFLOW__CORE__LOAD_EXAMPLES=False

if [ "$1" = "web" ]; then
    echo "Starting Airflow Webserver..."
    airflow webserver --port 8080
elif [ "$1" = "scheduler" ]; then
    echo "Starting Airflow Scheduler..."
    airflow scheduler
else
    echo "Usage: ./start_env.sh [web|scheduler]"
fi
