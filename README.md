# Tunisia Weather Pipeline — End-to-End Data Engineering Project

## Overview
This project implements an end-to-end data engineering pipeline for monitoring weather conditions across selected Tunisian cities.

It demonstrates the full data lifecycle:
- **Ingestion** from 2 distinct sources
- **Storage** of raw and transformed data
- **Transformation** and enrichment
- **Automated orchestration**
- **Restitution through an interactive dashboard**

## Data Sources
1. **Open-Meteo API**: current weather + daily forecast
2. **Local CSV metadata file**: Tunisian cities, regions, latitude, longitude

## Project Requirements Covered
- **2 sources distinctes**: API + CSV
- **Ingestion planifiée**: scheduled pipeline with APScheduler
- **Ingestion temps réel / quasi temps réel**: current weather fetched every 5 minutes
- **Architecture data**: raw JSON + SQLite analytical store
- **3+ transformations métier**:
  1. timestamp normalization
  2. temperature aggregation and derived metrics
  3. comfort/severity classification
  4. enrichment with regional metadata
- **Orchestration**: automated batch + stream-like jobs
- **Visualisation**: Streamlit dashboard
- **Qualité**: structured logging, retry logic, 5 tests
- **Déploiement**: Docker + docker-compose

## Architecture
See `docs/architecture.mmd`.

## Folder Structure
```text
weather_pipeline_project_full/
├── app.py
├── run_pipeline.py
├── scheduler.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── data/
│   ├── cities.csv
│   └── raw/
├── docs/
│   ├── architecture.mmd
│   ├── report_template.md
│   └── demo_script.md
├── src/
│   ├── config.py
│   ├── ingestion.py
│   ├── logging_config.py
│   ├── pipeline.py
│   ├── storage.py
│   └── transformation.py
└── tests/
    └── test_transformation.py
```
## Technology justification

SQLite was selected because the project is a local prototype with a small data volume. It avoids the overhead of configuring a PostgreSQL server while still providing structured SQL storage for the dashboard.

APScheduler was selected instead of Airflow because the pipeline has a limited number of tasks and does not require a heavy orchestration platform. It is enough to automate batch ingestion and near real-time polling.

Streamlit was selected because it allows fast development of an interactive data dashboard directly in Python, which is suitable for data engineering prototypes.

Docker was used to make the project reproducible and easy to run on another machine.

## Future improvements

In a production version, Kafka could be added to replace scheduled polling with true event-driven streaming. PostgreSQL or a cloud data warehouse could replace SQLite for better scalability. The dashboard could also be deployed publicly on Render, Railway, or a cloud VM.

## Quick Start (Local)
### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Run the initial pipeline
```bash
python run_pipeline.py
```

### 3) Start the dashboard
```bash
streamlit run app.py
```

### 4) Optional: start scheduler
```bash
python scheduler.py
```

## Docker Run
```bash
docker compose up --build
```
Then open:
```text
http://localhost:8501
```

## Tests
```bash
pytest -q
```

## Technology Stack and Justification
- **Python**: rapid development, strong ecosystem for data workflows
- **Requests**: reliable HTTP client for API ingestion
- **Pandas**: fast transformation and aggregation of tabular data
- **SQLite**: lightweight analytical store for local deployment
- **APScheduler**: simple orchestration and scheduling
- **Streamlit**: quick public-facing dashboard for data restitution
- **Docker**: reproducible local deployment
- **Pytest**: automated quality checks

## Suggested Presentation Summary
This project collects weather data from a public API and a local metadata file, stores raw and cleaned data, applies business transformations, automates updates, and exposes insights through an interactive dashboard.
