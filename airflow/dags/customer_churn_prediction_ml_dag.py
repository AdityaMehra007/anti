"""
Customer Churn Prediction ML DAG (Datasets & Deferrable Operators)
=================================================================
Demonstrates Airflow Data-Driven Scheduling triggered by Dataset updates
and asynchronous execution via Triggerer-backed Deferrable Operators.
"""

from datetime import datetime, timedelta
import logging

try:
    from airflow.decorators import dag, task
    from airflow.datasets import Dataset
    from airflow.operators.empty import EmptyOperator
except ImportError:
    pass

logger = logging.getLogger("airflow.ml")

raw_sales_dataset = Dataset("s3://omega-warehouse/raw_sales/v1")


@dag(
    dag_id="customer_churn_prediction_ml",
    schedule=[raw_sales_dataset],  # Data-driven scheduling
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ml", "churn", "datasets", "deferrable"]
)
def customer_churn_prediction_ml():

    @task(outlets=[raw_sales_dataset])
    def extract_raw_features() -> dict:
        logger.info("Extracting customer behavioral engagement vectors from Snowflake...")
        return {"feature_matrix_path": "s3://omega-warehouse/features/2026_10.parquet", "samples": 125000}

    @task(pool="heavy_compute_pool")
    def train_xgboost_deferred(features: dict) -> dict:
        logger.info(f"Submitting distributed XGBoost GPU training for {features['samples']} samples.")
        # Simulates deferring to Triggerer daemon
        return {"model_artifact_uri": "s3://omega-models/churn_xgb_v2.bin", "roc_auc": 0.942}

    @task
    def evaluate_roc_auc(metrics: dict) -> bool:
        logger.info(f"Evaluating model ROC-AUC: {metrics['roc_auc']}. Benchmark threshold = 0.90")
        if metrics["roc_auc"] >= 0.90:
            logger.info("Model qualifies for production staging.")
            return True
        raise ValueError("Model failed performance threshold.")

    @task
    def promote_to_triton_server(is_promoted: bool):
        if is_promoted:
            logger.info("Model promoted to Triton Inference Server cluster. Serving v2 endpoint.")

    feats = extract_raw_features()
    model = train_xgboost_deferred(feats)
    is_valid = evaluate_roc_auc(model)
    promote_to_triton_server(is_valid)


churn_dag = customer_churn_prediction_ml()
