# Technical Report — Tunisia Weather Monitoring Pipeline

---

## Table of Contents

1. [Context and Data Sources](#1-context-and-data-sources)
2. [Data Architecture and Technology Stack](#2-data-architecture-and-technology-stack)
3. [Annotated Pipeline Schema](#3-annotated-pipeline-schema)
4. [Main Transformations Performed](#4-main-transformations-performed)
5. [Difficulties Encountered and Solutions](#5-difficulties-encountered-and-solutions)
6. [Limitations and Future Improvements](#6-limitations-and-future-improvements)

---

## 1. Context and Data Sources

This project implements an end-to-end data engineering pipeline for monitoring weather conditions across multiple Tunisian cities.

The objective is to collect, process, and visualize weather data in order to provide useful insights such as temperature trends, forecasts, and alert conditions.

Two data sources are used:

| Source | Type | Description |
|--------|------|-------------|
| [Open-Meteo API](https://open-meteo.com/) | REST API | Real-time and forecast weather data — temperature, wind, precipitation, weather codes |
| `data/cities.csv` | Local file | Tunisian cities metadata — names, regions, and geographic coordinates |

The combination of these two sources allows the system to enrich raw weather data with contextual geographic information.

---

## 2. Data Architecture and Technology Stack

### Architecture Overview

A lightweight architecture was chosen to prioritize clarity and ease of deployment:

| Layer | Implementation |
|-------|---------------|
| Raw Layer | JSON files stored locally |
| Processed Layer | SQLite database |
| Serving Layer | Streamlit dashboard |

This structure enforces a clean separation between raw and processed data while keeping the system simple and reproducible.

### Technology Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core pipeline language |
| Requests | API data ingestion |
| Pandas | Data transformation and aggregation |
| SQLite | Structured storage for processed data |
| APScheduler | Automated pipeline scheduling |
| Streamlit | Interactive dashboard |
| Docker | Reproducibility and portability |
| Pytest | Automated testing |

### Design Decisions

**SQLite** was selected because the project is a local prototype with a limited data volume. It provides structured SQL storage without the overhead of running a database server.

**APScheduler** was used instead of heavier orchestration tools such as Airflow because the pipeline has a small number of tasks and does not require complex dependency management.

**Streamlit** enables fast creation of interactive dashboards directly in Python, with no frontend development required.

**Docker** ensures the application runs consistently across different environments.

---

## 3. Annotated Pipeline Schema

```
┌─────────────────────┐     ┌─────────────────────┐
│   Open-Meteo API    │     │   data/cities.csv    │
└────────┬────────────┘     └──────────┬──────────┘
         │                             │
         └──────────┬──────────────────┘
                    ▼
         ┌─────────────────────┐
         │  Ingestion Phase    │  Fetch weather data per city
         └────────┬────────────┘
                  ▼
         ┌─────────────────────┐
         │  Raw Storage Phase  │  Save API responses as JSON files
         └────────┬────────────┘
                  ▼
         ┌─────────────────────┐
         │ Transformation Phase│  Clean and enrich data with Pandas
         └────────┬────────────┘
                  ▼
         ┌─────────────────────┐
         │  Processed Storage  │  Store structured records in SQLite
         └────────┬────────────┘
                  ▼
         ┌─────────────────────┐
         │ Streamlit Dashboard │  Read from SQLite and visualize
         └─────────────────────┘
```

The pipeline runs automatically on a 5-minute schedule via APScheduler.

**Ingestion Phase** — Weather data is fetched from the Open-Meteo API for each city defined in the CSV file.

**Raw Storage Phase** — API responses are saved as JSON files, enabling traceability and the ability to reprocess data without re-fetching.

**Transformation Phase** — Data is cleaned, normalized, and enriched using Pandas. Derived fields are computed at this stage.

**Processed Storage Phase** — Transformed records are written to structured SQLite tables.

**Visualization Phase** — The Streamlit dashboard reads from SQLite and renders tables, charts, and alerts.

---

## 4. Main Transformations Performed

### Data Cleaning and Normalization

- Standardization of timestamps to a consistent format
- Formatting and rounding of numerical weather values

### Aggregation and Derived Metrics

- Calculation of average temperature per city and region
- Extraction of daily minimum and maximum temperatures

### Data Enrichment

- Merging raw weather data with city metadata from `cities.csv`
- Adding region information to each weather record

### Classification

- Assignment of comfort levels: `cold`, `comfortable`, `hot`
- Detection of alert conditions based on wind speed thresholds or severe weather codes

---

## 5. Difficulties Encountered and Solutions

| Difficulty | Solution |
|------------|----------|
| Handling multiple data sources with different schemas | Defined a unified internal schema to merge API data with CSV metadata |
| Ensuring reliable API calls | Implemented retry logic to handle transient failures gracefully |
| Designing a simple orchestration system | Used APScheduler instead of heavier tools — sufficient for the pipeline's complexity |
| Balancing simplicity and completeness | Selected lightweight tools that still cover all pipeline stages end-to-end |

---

## 6. Limitations and Future Improvements

### Current Limitations

| Limitation | Detail |
|------------|--------|
| No true real-time streaming | The pipeline uses scheduled polling every 5 minutes — not event-driven |
| Local deployment only | The dashboard is not publicly accessible |
| SQLite scalability | Not suitable for high-volume or concurrent production workloads |

### Future Improvements

- **Kafka** — replace polling with real-time event-driven ingestion
- **PostgreSQL or cloud data warehouse** — replace SQLite for scalability (e.g. BigQuery, Redshift)
- **Public deployment** — host the dashboard on Render, Railway, or a cloud VM
- **Historical analysis and anomaly detection** — extend the dashboard with trend analysis

### Note on Real-Time Processing

The project implements near real-time ingestion by fetching data every 5 minutes using scheduled tasks. This approach simulates streaming behavior in a simple and deployment-friendly way suitable for a prototype context.
