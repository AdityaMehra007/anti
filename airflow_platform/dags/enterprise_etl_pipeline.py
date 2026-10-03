"""
Enterprise ETL Pipeline
Demonstrating TaskFlow API, Dynamic Task Mapping, Retry Policies, and typed XCom exchanges.
"""

from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any, Dict, List

# Airflow imports
try:
    from airflow.decorators import dag, task
    from airflow.models.baseoperator import chain
except ImportError:
    # Stub decorator support for standalone static validation environments
    def dag(*args, **kwargs):
        def decorator(f):
            return f
        return decorator

    def task(*args, **kwargs):
        def decorator(f):
            f.expand = lambda **k: f
            return f
        return decorator

logger = logging.getLogger("airflow.task")

default_args = {
    "owner": "data_platform",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(seconds=30),
    "execution_timeout": timedelta(minutes=15),
}


@dag(
    dag_id="enterprise_etl_pipeline",
    default_args=default_args,
    description="Production-grade TaskFlow pipeline with Dynamic Task Mapping and Data Validation",
    schedule="0 4 * * *",  # Daily at 04:00 UTC
    start_date=datetime(2025, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["production", "etl", "financial_data"],
)
def enterprise_etl_pipeline():

    @task(task_id="discover_partitions")
    def discover_partitions() -> List[str]:
        """Discovers uningested partition batches."""
        batches = [f"batch_2026_10_03_partition_{i:02d}" for i in range(1, 4)]
        logger.info(f"Discovered {len(batches)} partition batches for parallel processing.")
        return batches

    @task(task_id="extract_and_transform_partition")
    def extract_and_transform(partition_id: str) -> Dict[str, Any]:
        """Processes an individual partition in an isolated mapped task instance."""
        logger.info(f"Ingesting partition payload: {partition_id}")
        # Synthetic data generation & transformation logic
        records_processed = 12500
        gross_volume = 4850000.75
        return {
            "partition": partition_id,
            "record_count": records_processed,
            "volume_usd": gross_volume,
            "status": "TRANSFORMED",
        }

    @task(task_id="validate_quality_gate")
    def validate_quality_gate(partition_summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Performs data quality assertions across all transformed partitions."""
        total_records = sum(item["record_count"] for item in partition_summaries)
        total_usd = sum(item["volume_usd"] for item in partition_summaries)

        if total_records == 0:
            raise ValueError("Data Quality Check Failed: Zero records ingested across partitions.")

        logger.info(
            f"Quality Gate PASSED. Total Records: {total_records:,}, Aggregated Volume: ${total_usd:,.2f}"
        )
        return {
            "passed": True,
            "total_records": total_records,
            "aggregated_volume_usd": total_usd,
            "partition_count": len(partition_summaries),
        }

    @task(task_id="publish_lineage_and_metrics")
    def publish_lineage(metrics: Dict[str, Any]):
        """Publishes final operational metrics and emits lineage confirmation."""
        logger.info(f"ETL Execution complete. Final Metrics Ledger: {metrics}")

    # DAG Dependency Topology
    raw_partitions = discover_partitions()
    # Dynamic Task Mapping (AIP-42): Each partition spawns a separate mapped task
    processed_partitions = extract_and_transform.expand(partition_id=raw_partitions)
    validated_metrics = validate_quality_gate(processed_partitions)
    publish_lineage(validated_metrics)


# Instantiate the DAG
pipeline_instance = enterprise_etl_pipeline()
