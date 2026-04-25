# Tunisia Weather Pipeline — End-to-End Data Engineering Project

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Docker](https://img.shields.io/badge/Docker-ready-informational)
![License](https://img.shields.io/badge/License-MIT-green)

## 1. Project Description and Use Case

This project implements an end-to-end data engineering pipeline for monitoring weather conditions across selected Tunisian cities.

The goal is to demonstrate the full data lifecycle:
- Data ingestion from multiple sources  
- Data storage (raw and structured)  
- Data transformation and enrichment  
- Automated pipeline execution  
- Data visualization through a dashboard  

Use case: provide near real-time weather insights and forecasts for different regions in Tunisia.

---

## 2. Architecture Diagram

See the architecture diagram in: [`docs/architecture.mmd`](docs/architecture.mmd)

This diagram illustrates the flow from data ingestion to storage, transformation, and visualization.

Pipeline flow:
1. Data ingestion from API and CSV  
2. Raw data stored as JSON files  
3. Data transformation using Pandas  
4. Processed data stored in SQLite  
5. Dashboard reads processed data  

---

## 3. Data Sources Used

1. Open-Meteo API  
Provides current weather and forecast data  

2. Local CSV file (data/cities.csv)  
Contains Tunisian cities metadata (region, latitude, longitude)  

---

## 4. Technology Stack and Justifications

- Python: rapid development and strong ecosystem  
- Requests: API data ingestion  
- Pandas: data transformation and aggregation  
- SQLite: lightweight structured storage  
- APScheduler: pipeline scheduling  
- Streamlit: interactive dashboard  
- Docker: reproducible deployment  
- Pytest: automated tests  

### Justification

SQLite was selected because the project is a local prototype with limited data volume. It avoids the overhead of configuring a full database server while still providing SQL capabilities.

APScheduler was chosen instead of Airflow because the pipeline is simple and does not require a heavy orchestration tool.

Streamlit allows fast development of a dashboard without frontend complexity.

Docker ensures the project runs consistently across different environments.

---

## 5. Installation Instructions

### Local Setup

Install dependencies:
pip install -r requirements.txt

Run pipeline:
python run_pipeline.py

Run dashboard:
streamlit run app.py

---

### Docker Setup

docker compose up --build

Open:
http://localhost:8501

---

## 6. Deployment / Access

Dashboard URL:
http://localhost:8501

No credentials or API keys are required to run the project locally.

---

## 7. Dashboard Usage

The dashboard provides:
- Current weather per city  
- Temperature trends  
- Forecast data  
- Regional summaries  
- Alert monitoring  

Data is updated automatically using scheduled ingestion.

---

## 8. Tests

Run tests with:
pytest -q

The project includes at least 5 tests covering transformation logic.

---

## 9. Limitations and Future Improvements

### Limitations
- No true streaming system (Kafka)  
- Local deployment only  
- SQLite not scalable for large datasets  

### Future Improvements
- Add Kafka for real-time streaming  
- Replace SQLite with PostgreSQL or cloud warehouse  
- Deploy dashboard publicly  

Note:
The project uses near real-time ingestion (every 5 minutes) through scheduled polling to simulate streaming.

---

## 10. Summary

This project demonstrates a complete data engineering pipeline from ingestion to visualization using a simple and effective architecture suitable for prototyping.
