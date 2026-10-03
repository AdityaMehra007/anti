"""
Deferrable Operators & Async Triggerer Pipeline
Demonstrates yielding worker compute slots during long-polling external states.
"""

from __future__ import annotations

from datetime import datetime, timedelta
import logging

try:
    from airflow.decorators import dag, task
    from airflow.sensors.time_sensor import TimeSensorAsync
    from airflow.operators.empty import EmptyOperator
except ImportError:
    def dag(*args, **kwargs):
        def decorator(f):
            return f
        return decorator

    def task(*args, **kwargs):
        def decorator(f):
            return f
        return decorator

    class EmptyOperator:
        def __init__(self, *args, **kwargs):
            pass

    class TimeSensorAsync:
        def __init__(self, *args, **kwargs):
            pass

logger = logging.getLogger("airflow.task")


@dag(
    dag_id="deferrable_async_pipeline",
    schedule="0 6 * * *",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["deferrable", "async", "triggerer"],
)
def deferrable_async_pipeline():

    @task(task_id="submit_heavy_remote_job")
    def submit_remote_job() -> str:
        job_id = "job_spark_cluster_run_9941"
        logger.info(f"Submitted remote computational job: {job_id}")
        return job_id

    # Simulated Deferrable Sensor:
    # Instead of blocking a worker slot for minutes, this yields execution to the Triggerer
    async_barrier = TimeSensorAsync(
        task_id="wait_for_window_async",
        target_time=(datetime.utcnow() + timedelta(seconds=10)).time(),
    )

    @task(task_id="harvest_remote_results")
    def harvest_results(job_id: str):
        logger.info(f"Worker resumed execution via Triggerer event. Harvesting payload for {job_id}")
        return {"exit_code": 0, "rows_computed": 150000}

    job = submit_remote_job()
    job >> async_barrier
    harvest_results(job)


deferrable_pipeline_instance = deferrable_async_pipeline()
