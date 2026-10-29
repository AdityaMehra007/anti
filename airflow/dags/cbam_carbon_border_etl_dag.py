"""
CBAM Carbon Border ETL DAG (Dynamic Task Mapping)
=================================================
Demonstrates modern Airflow 2.x/3.0 Dynamic Task Mapping (.expand())
over international cargo customs declarations.
"""

from datetime import datetime, timedelta
import logging

try:
    from airflow.decorators import dag, task
    from airflow.datasets import Dataset
except ImportError:
    pass

logger = logging.getLogger("airflow.cbam")

cbam_dataset = Dataset("postgres://omega_analytics/cbam_dockets/v1")


@dag(
    dag_id="cbam_carbon_border_etl",
    schedule_interval="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["exim", "cbam", "dynamic_mapping", "trade"]
)
def cbam_carbon_border_etl():

    @task(outlets=[cbam_dataset])
    def ingest_customs_declarations() -> list[dict]:
        logger.info("Ingesting EU customs declaration dockets...")
        return [
            {"docket_id": "DKT-2026-001", "cn_code": "7307", "net_mass_kg": 24500.0, "origin": "IN"},
            {"docket_id": "DKT-2026-002", "cn_code": "7601", "net_mass_kg": 18200.0, "origin": "IN"},
            {"docket_id": "DKT-2026-003", "cn_code": "7208", "net_mass_kg": 42000.0, "origin": "VN"}
        ]

    @task(pool="heavy_compute_pool")
    def process_docket_tariff(docket: dict) -> dict:
        multiplier = 1.385  # EUR per metric ton CO2 equivalent
        co2_tons = (docket["net_mass_kg"] / 1000.0) * 1.85
        tariff_eur = round(co2_tons * multiplier * 78.50, 2)
        logger.info(f"Docket {docket['docket_id']} (CN: {docket['cn_code']}): Carbon Tariff = €{tariff_eur}")
        return {"docket_id": docket["docket_id"], "tariff_eur": tariff_eur}

    @task
    def aggregate_cbam_liability(tariffs: list[dict]):
        total_eur = sum(t["tariff_eur"] for t in tariffs)
        logger.info(f"Total aggregated EU CBAM liability across all shipments: €{total_eur}")
        return {"total_liability_eur": total_eur, "shipment_count": len(tariffs)}

    dockets = ingest_customs_declarations()
    # Dynamic Task Mapping .expand()
    processed_tariffs = process_docket_tariff.expand(docket=dockets)
    aggregate_cbam_liability(processed_tariffs)


cbam_dag = cbam_carbon_border_etl()
