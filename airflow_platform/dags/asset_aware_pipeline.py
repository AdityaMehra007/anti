"""
Asset-Aware Producer-Consumer Pipelines
Demonstrating data-driven event scheduling using Airflow Assets / Datasets (AIP-44 / AIP-60).
"""

from __future__ import annotations

from datetime import datetime, timedelta
import logging

try:
    from airflow.decorators import dag, task
    try:
        from airflow.sdk import Asset
    except ImportError:
        from airflow.datasets import Dataset as Asset
except ImportError:
    class Asset:
        def __init__(self, uri: str):
            self.uri = uri

    def dag(*args, **kwargs):
        def decorator(f):
            return f
        return decorator

    def task(*args, **kwargs):
        def decorator(f):
            return f
        return decorator

logger = logging.getLogger("airflow.task")

# Canonical Asset URIs (AIP-60 standardized representation)
RAW_TELEMETRY_ASSET = Asset("s3://data-lake-lakehouse/bronze/telemetry.parquet")
PROCESSED_METRICS_ASSET = Asset("postgres://analytics_warehouse/gold/hourly_fleet_kpis")


# ==========================================
# 1. Producer DAG: Ingests & Emits Asset
# ==========================================
@dag(
    dag_id="asset_producer_telemetry_ingest",
    schedule="*/30 * * * *",  # Scheduled every 30 minutes
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["asset_aware", "producer", "telemetry"],
)
def producer_pipeline():

    @task(outlets=[RAW_TELEMETRY_ASSET])
    def fetch_and_write_telemetry():
        logger.info("Ingesting device telemetry into bronze S3 location.")
        # Emits update to RAW_TELEMETRY_ASSET on successful termination
        return {"records_staged": 8420}

    fetch_and_write_telemetry()


producer_pipeline_instance = producer_pipeline()


# ==========================================
# 2. Consumer DAG: Triggered Exclusively by Asset Updates
# ==========================================
@dag(
    dag_id="asset_consumer_metrics_aggregator",
    schedule=[RAW_TELEMETRY_ASSET],  # Triggered immediately when Producer updates asset!
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["asset_aware", "consumer", "analytics"],
)
def consumer_pipeline():

    @task(outlets=[PROCESSED_METRICS_ASSET])
    def calculate_fleet_kpis():
        logger.info("Executing downstream aggregation triggered by new Telemetry Asset.")
        return {"kpis_generated": 14}

    calculate_fleet_kpis()


consumer_pipeline_instance = consumer_pipeline()
