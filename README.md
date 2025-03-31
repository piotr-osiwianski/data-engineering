# Airflow ETL Project with SQLite

## 🔧 Project Overview

This repository contains a simple ETL pipeline using Apache Airflow and SQLite. The DAGs included are:

- `etl_csv_to_sqlite`: Main DAG that loads data from `customers.csv`, cleans it, and inserts into `mydata.db`
- `test_logging_dag`: Minimal DAG that writes a test log to ensure Airflow is running correctly

---

## 📁 Project Structure

```
.
├── dags/
│   ├── etl_csv_to_sqlite.py
│   └── test_logging_dag.py
├── data/
│   └── customers.csv
├── airflow_home/ (created automatically)
├── start_env.sh
├── stop_all.sh
├── README.md
├── airflow_ui.png
```

---

## ▶️ How to Run (Mac/Linux). I can also use Docker instead of installing it in Terminal. 

### 1. Create virtual environment & install Airflow

```bash
python3 -m venv venv
source venv/bin/activate
pip install "apache-airflow==2.8.0" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.0/constraints-3.9.txt"
```

### 2. Initialize Airflow and create user (first time only)

```bash
export AIRFLOW_HOME=$(pwd)/airflow_home
airflow db init
airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

### 3. Start services using bash script:

#### Terminal 1 – Webserver:
```bash
./start_env.sh web
```

#### Terminal 2 – Scheduler:
```bash
./start_env.sh scheduler
```

Then go to: [http://localhost:8080](http://localhost:8080)  
Login: `admin` / `admin`


### 3.1 Start services using commands:

### Terminal 1: Starting Webserver

```bash
cd "/Users/piotrek/Desktop/Apache Airflow/airflow_sqlite_etl"
source venv/bin/activate
export AIRFLOW_HOME=$(pwd)/airflow_home
export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/dags
# (Tylko przy pierwszym uruchomieniu lub po czyszczeniu bazy)
airflow db init
# Add user (only once, if does not exist)
airflow users create \
  --username admin \
  --firstname Piotrek \
  --lastname Admin \
  --role Admin \
  --email piotrek@example.com \
  --password admin

# Teraz dopiero uruchamiam webserver:
airflow webserver --port 8080
```

### Terminal 2: Starting Scheduler

```bash
cd "/Users/piotrek/Desktop/Apache Airflow/airflow_sqlite_etl"
source venv/bin/activate
export AIRFLOW_HOME=$(pwd)/airflow_home
export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/dags
airflow scheduler
```

---

## ✅ Test the DAGs in Airflow UI 

### Run `test_logging_dag`
This will write `Hello from Airflow!` to `data/hello_log.txt`

### Run `etl_csv_to_sqlite`
This will:
- Read `data/customers.csv`
- Clean invalid rows
- Load valid entries into `data/mydata.db` → table `customers`

---

## 🛑 To stop all Airflow processes:

```bash
./stop_all.sh
```

---

