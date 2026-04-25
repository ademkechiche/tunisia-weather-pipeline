# Demo Script (3–5 minutes)

## Introduction
Hello, this project is an end-to-end data engineering pipeline for monitoring weather conditions in Tunisian cities.

## Data Sources
The first source is the Open-Meteo API, which provides current weather and forecast data.
The second source is a local CSV file containing city metadata such as name, region, latitude, and longitude.

## Pipeline
The ingestion layer fetches the API data, saves the raw JSON files, then transforms and enriches the data using Pandas.
The cleaned data is stored in SQLite.
Scheduling is handled by APScheduler for both batch and near real-time updates.

## Dashboard
On the dashboard, we can see current metrics, forecast temperature trends, precipitation charts, regional summaries, and alert levels.

## Quality
The project includes structured logs, retry logic, Docker deployment, and 5 automated tests.

## Conclusion
This pipeline covers the full data lifecycle from ingestion to visualization and can be extended later with cloud deployment and real streaming tools such as Kafka.
