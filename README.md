# Tunisia Weather Pipeline — End-to-End Data Engineering Project

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-FF4B4B?logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-storage-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Table of Contents

1. [Project Description](#1-project-description)
2. [Architecture](#2-architecture)
3. [Data Sources](#3-data-sources)
4. [Technology Stack](#4-technology-stack)
5. [Installation](#5-installation)
6. [Dashboard Usage](#6-dashboard-usage)
7. [Tests](#7-tests)
8. [Limitations & Future Improvements](#8-limitations--future-improvements)

---

## 1. Project Description

This project implements an end-to-end data engineering pipeline for monitoring weather conditions across selected Tunisian cities.

The goal is to demonstrate the full data lifecycle:

- **Ingestion** — pulling data from a live REST API and a local CSV file
- **Storage** — persisting raw data as JSON files before transformation
- **Transformation** — cleaning and enriching data with Pandas
- **Scheduling** — automated pipeline execution every 5 minutes
- **Visualization** — interactive dashboard for weather insights

**Use case:** provide near real-time weather insights and forecasts for different regions in Tunisia.

---

## 2. Architecture

```
Open-Meteo API ──┐
                 ├──► Raw JSON files ──► Pandas transform ──► SQLite ──► Streamlit dashboard
data/cities.csv ─┘
```

Pipeline flow:

1. Weather data is fetched from the Open-Meteo API and city metadata is loaded from `data/cities.csv`
2. Raw API responses are saved as JSON files for auditability
3. Pandas transforms and enriches the raw data
4. Processed records are stored in SQLite
5. The Streamlit dashboard reads from SQLite and refreshes automatically

Full diagram: [`docs/architecture.mmd`](docs/architecture.mmd)

---

## 3. Data Sources

| Source | Type | Description |
|--------|------|-------------|
| [Open-Meteo API](https://open-meteo.com/) | REST API | Current weather and forecast data — no API key required |
| `data/cities.csv` | Local file | Tunisian cities metadata: name, region, latitude, longitude |

---

## 4. Technology Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11 | Core language |
| Requests | latest | API data ingestion |
| Pandas | latest | Data transformation and aggregation |
| SQLite | built-in | Lightweight structured storage |
| APScheduler | latest | Pipeline scheduling |
| Streamlit | latest | Interactive dashboard |
| Docker | latest | Reproducible containerized deployment |
| Pytest | latest | Automated testing |

### Design decisions

**SQLite** was selected because this is a local prototype with limited data volume. It provides full SQL capabilities without the overhead of running a database server.

**APScheduler** was chosen over Airflow because the pipeline is simple and linear — a heavy orchestration framework would add unnecessary complexity.

**Streamlit** enables rapid dashboard development without any frontend engineering, which is appropriate for a prototyping context.

**Docker** ensures the project runs identically across different machines and operating systems.

---

## 5. Installation

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized setup)

### Option A — Local setup

```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-folder>

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python pipeline.py

# Launch the dashboard (in a separate terminal)
streamlit run app.py
```

### Option B — Docker setup

```bash
docker compose up --build
```

Then open your browser at:

```
http://localhost:8501
```

> No API keys or credentials are required to run the project locally.

---

## 6. Dashboard Usage

The dashboard is available at `http://localhost:8501` and provides:

- **Current weather** — temperature, humidity, and wind speed per city
- **Temperature trends** — historical charts by city and region
- **Forecast data** — upcoming conditions from the Open-Meteo forecast endpoint
- **Regional summaries** — aggregated statistics across Tunisian regions
- **Alert monitoring** — flags for extreme temperature or wind conditions

Data is refreshed automatically every 5 minutes through the scheduled pipeline.

---

## 7. Tests

```bash
pytest -q
```

The test suite includes at least 5 tests covering:

- Field validation on ingested data
- Transformation logic correctness
- Aggregation accuracy
- Edge case handling (missing fields, empty API responses)

---

## 8. Limitations & Future Improvements

### Current limitations

| Limitation | Detail |
|------------|--------|
| No true streaming | The pipeline uses scheduled polling every 5 minutes to simulate near real-time ingestion — not event-driven |
| Local deployment only | The dashboard is not publicly accessible |
| SQLite scalability | Not suitable for high-volume or concurrent workloads |

### Planned improvements

- **Kafka** — replace polling with real-time event streaming
- **PostgreSQL or cloud warehouse** — replace SQLite for scalability (e.g. BigQuery, Redshift)
- **Public deployment** — host the dashboard on Streamlit Cloud or a cloud provider
- **Data quality checks** — integrate Great Expectations or dbt tests
- **CI/CD pipeline** — automate testing and deployment on push

---

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
