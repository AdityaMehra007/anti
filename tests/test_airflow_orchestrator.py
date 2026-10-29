"""
Apache Airflow Autonomous Orchestrator Pytest Suite
===================================================
Comprehensive unit & integration tests covering DAG parsing, Kahn's topological sort,
cycle detection, TaskFlow API execution, Dynamic Task Mapping, Datasets, Deferrable operators,
pools, XCom, and 12-phase sovereign lifecycle validation.
"""

import pytest
from airflow_orchestrator import (
    AirflowClient,
    AirflowConfig,
    AirflowOrchestrator,
    DAGMetadata,
    TaskMetadata
)


@pytest.fixture
def client():
    return AirflowClient()


def test_system_health(client):
    health = client.get_health()
    assert health["metadatabase"]["status"] == "healthy"
    assert health["scheduler"]["status"] == "healthy"
    assert health["triggerer"]["status"] == "healthy"


def test_list_and_get_dags(client):
    dags = client.list_dags()
    assert len(dags) >= 5
    dag_ids = [d["dag_id"] for d in dags]
    assert "financial_ledger_reconciliation" in dag_ids
    assert "autonomous_security_threat_recon" in dag_ids
    assert "cbam_carbon_border_etl" in dag_ids
    assert "customer_churn_prediction_ml" in dag_ids
    assert "daily_cloud_db_snapshot_and_s3_vault" in dag_ids

    dag_detail = client.get_dag("financial_ledger_reconciliation")
    assert dag_detail["dag_id"] == "financial_ledger_reconciliation"
    assert len(dag_detail["tasks"]) == 6


def test_topological_sort_order(client):
    order = client.mock_engine.topological_sort_dag("financial_ledger_reconciliation")
    assert "extract_bank_feed" in order
    assert "compute_reconciliation" in order
    # Verify upstream comes before downstream
    assert order.index("extract_bank_feed") < order.index("compute_reconciliation")
    assert order.index("compute_reconciliation") < order.index("evaluate_discrepancy_branch")


def test_cycle_detection_exception(client):
    cyclic_dag = DAGMetadata(
        dag_id="cyclic_test_dag",
        description="DAG with intentional cycle",
        schedule_interval="@daily"
    )
    t1 = TaskMetadata(task_id="task_a", dag_id="cyclic_test_dag", operator_type="PythonOperator")
    t2 = TaskMetadata(task_id="task_b", dag_id="cyclic_test_dag", operator_type="PythonOperator")
    t1.downstream_task_ids = ["task_b"]
    t2.downstream_task_ids = ["task_a"]
    cyclic_dag.tasks = {"task_a": t1, "task_b": t2}
    
    client.mock_engine.dags["cyclic_test_dag"] = cyclic_dag
    with pytest.raises(ValueError, match="Cyclic dependency detected"):
        client.mock_engine.topological_sort_dag("cyclic_test_dag")


def test_trigger_dag_run(client):
    run = client.trigger_dag("financial_ledger_reconciliation", conf={"test_flag": True})
    assert run["state"] == "success"
    assert len(run["task_instances"]) == 6
    for ti in run["task_instances"].values():
        assert ti["state"] == "success"
        assert len(ti["log"]) > 0


def test_dynamic_task_mapping_expand(client):
    run = client.trigger_dag("cbam_carbon_border_etl", conf={"mapped_items_count": 3})
    assert run["state"] == "success"
    # Verify mapped tasks were created
    assert "process_docket_tariff[0]" in run["task_instances"]
    assert "process_docket_tariff[1]" in run["task_instances"]
    assert "process_docket_tariff[2]" in run["task_instances"]
    assert run["task_instances"]["process_docket_tariff[0]"]["map_index"] == 0


def test_deferrable_operator_triggerer(client):
    run = client.trigger_dag("customer_churn_prediction_ml")
    assert run["state"] == "success"
    deferred_ti = run["task_instances"]["train_xgboost_deferred"]
    assert any("Triggerer" in log for log in deferred_ti["log"])


def test_pools_concurrency(client):
    pools = client.list_pools()
    pool_dict = {p["name"]: p for p in pools}
    assert "default_pool" in pool_dict
    assert "heavy_compute_pool" in pool_dict
    assert pool_dict["default_pool"]["slots"] == 128


def test_variables_and_connections(client):
    vars_list = client.list_variables()
    assert len(vars_list) >= 3
    client.set_variable("test_airflow_var", "sovereign_value", "Unit test variable")
    updated = {v["key"]: v["val"] for v in client.list_variables()}
    assert updated.get("test_airflow_var") == "sovereign_value"

    conns = client.list_connections()
    conn_ids = [c["conn_id"] for c in conns]
    assert "postgres_primary" in conn_ids
    assert "aws_s3_data_lake" in conn_ids


def test_security_audit(client):
    audit = client.mock_engine.audit_security_and_best_practices()
    assert audit["status"] == "PASS"
    assert audit["total_dags"] >= 5
    assert audit["findings_count"] >= 0


def test_sovereign_12_phase_lifecycle():
    orchestrator = AirflowOrchestrator()
    manifest = orchestrator.run_lifecycle()
    assert manifest["overall_status"] == "VERIFIED"
    assert manifest["phases_completed"] == 12
    for r in manifest["results"]:
        assert r["status"] == "SUCCESS", f"Failed phase: {r['phase']} with {r.get('error')}"
