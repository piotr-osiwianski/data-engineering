#!/bin/bash
# Script: stop_all.sh
# Purpose: Stop all running Airflow processes

echo "Stopping all Airflow processes..."
pkill -f "airflow"
