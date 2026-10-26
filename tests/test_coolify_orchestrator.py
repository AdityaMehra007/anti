"""
Unit & Integration Tests for Coolify Autonomous Orchestrator Suite
==================================================================
Tests client initialization, server validation, project/application lifecycle,
database provisioning, template catalog searching, deployment queues, and CLI commands.
"""

import os
import pytest
from coolify_orchestrator import (
    CoolifyConfig,
    CoolifyClient,
    CoolifyOrchestrator,
    CoolifyTemplateCatalog,
    CoolifyMockEngine
)
import coolify_cli


@pytest.fixture
def mock_client():
    config = CoolifyConfig(mock_mode=True)
    return CoolifyClient(config)


@pytest.fixture
def orchestrator(mock_client):
    return CoolifyOrchestrator(mock_client)


def test_mock_engine_initial_state():
    engine = CoolifyMockEngine()
    assert engine.get_version().startswith("4.")
    health = engine.healthcheck()
    assert health["status"] == "ok"
    assert len(engine.servers) >= 2
    assert len(engine.applications) >= 2
    assert len(engine.databases) >= 3


def test_client_version_and_health(mock_client):
    version = mock_client.get_version()
    assert "4." in version
    health = mock_client.healthcheck()
    assert health.get("status") == "ok"


def test_server_listing_and_validation(mock_client):
    servers = mock_client.list_servers()
    assert isinstance(servers, list)
    assert len(servers) >= 2
    
    localhost_srv = servers[0]
    assert localhost_srv["name"] == "localhost"
    assert localhost_srv["ip"] == "127.0.0.1"

    validation = mock_client.validate_server(localhost_srv["uuid"])
    assert validation["status"] == "validated"
    assert "docker_version" in validation
    assert validation["memory_total_mb"] > 0


def test_server_docker_cleanup(mock_client):
    res = mock_client.cleanup_docker("srv-localhost-000")
    assert res.get("status") == "ok"


def test_project_lifecycle(mock_client):
    projects_before = len(mock_client.list_projects())
    new_proj = mock_client.create_project("Test Autonomous Cloud", "Isolated testing environment")
    assert new_proj["name"] == "Test Autonomous Cloud"
    assert new_proj["uuid"].startswith("prj-")
    assert len(new_proj["environments"]) >= 1

    projects_after = len(mock_client.list_projects())
    assert projects_after == projects_before + 1


def test_application_lifecycle_and_deploy(mock_client):
    app = mock_client.create_application(
        name="test-microservice",
        git_repository="https://github.com/coollabsio/coolify",
        git_branch="main",
        build_pack="nixpacks",
        fqdn="https://test-microservice.local",
        ports_exposes="8000"
    )
    assert app["name"] == "test-microservice"
    assert app["uuid"].startswith("app-")
    assert app["status"] == "stopped"

    # Trigger deployment
    dep = mock_client.deploy(app["uuid"], force_rebuild=True)
    assert "deployment_uuid" in dep
    assert dep["status"] == "queued"

    # Verify status changed to running
    dep_status = mock_client.get_deployment_status(dep["deployment_uuid"])
    assert len(dep_status["logs"]) > 0


def test_database_provisioning(mock_client):
    dbs_before = len(mock_client.list_databases())
    
    pg_db = mock_client.create_database("postgresql", "test-postgres")
    assert pg_db["type"] == "standalone-postgresql"
    assert pg_db["name"] == "test-postgres"

    redis_db = mock_client.create_database("redis", "test-redis")
    assert redis_db["type"] == "standalone-redis"

    dbs_after = len(mock_client.list_databases())
    assert dbs_after == dbs_before + 2


def test_service_catalog_search():
    catalog = CoolifyTemplateCatalog()
    assert len(catalog.services) > 0

    # Search for AI services
    ai_services = catalog.search(query="ai")
    assert len(ai_services) > 0

    # Search for exact service
    n8n_matches = catalog.search(query="n8n")
    assert len(n8n_matches) >= 1
    assert any(m["id"] == "n8n" for m in n8n_matches)

    # Search by category
    db_services = catalog.search(category="database")
    assert len(db_services) > 0


def test_orchestrator_cluster_status(orchestrator):
    status = orchestrator.get_cluster_status()
    assert status["status"] in ("healthy", "degraded")
    assert status["total_servers"] >= 2
    assert status["healthy_servers"] >= 2
    assert status["total_applications"] >= 2
    assert status["total_databases"] >= 3
    assert status["catalog_template_count"] > 0


def test_orchestrator_stack_provision(orchestrator):
    res = orchestrator.provision_full_omega_stack()
    assert res["status"] == "provisioned"
    assert res["project"]["name"] == "OMEGA Autonomous Core"
    assert len(res["databases"]) == 2
    assert len(res["services"]) == 1


def test_cli_execution_commands(orchestrator, mock_client, capsys):
    # Test cmd_info
    coolify_cli.cmd_info(orchestrator, None)
    out = capsys.readouterr().out
    assert "COOLIFY CLUSTER SUMMARY & TELEMETRY" in out

    # Test cmd_servers
    coolify_cli.cmd_servers(mock_client, None)
    out = capsys.readouterr().out
    assert "srv-localhost-000" in out

    # Test cmd_apps
    coolify_cli.cmd_apps(mock_client, None)
    out = capsys.readouterr().out
    assert "app-omega-api" in out

    # Test cmd_dbs
    coolify_cli.cmd_dbs(mock_client, None)
    out = capsys.readouterr().out
    assert "db-coolify-internal" in out

    # Test cmd_catalog
    class Args:
        search = "n8n"
        category = ""
    coolify_cli.cmd_catalog(orchestrator, Args())
    out = capsys.readouterr().out
    assert "n8n" in out


def test_compose_exporter_and_magic_interpolation(tmp_path):
    from coolify_compose_exporter import CoolifyComposeExporter
    exporter = CoolifyComposeExporter()
    
    # Test export for anythingllm
    raw_compose, env_dict = exporter.export("anythingllm", domain="test.local")
    assert "mintplexlabs/anythingllm" in raw_compose
    assert "SERVICE_PASSWORD_JWTSECRET" in env_dict
    assert len(env_dict["SERVICE_PASSWORD_JWTSECRET"]) > 10

    # Test saving stack to temp directory
    out_dir = str(tmp_path / "anythingllm")
    save_res = exporter.save_stack("anythingllm", out_dir, domain="test.local")
    assert int(save_res["total_vars"]) >= 10
    assert os.path.exists(save_res["compose_path"])
    assert os.path.exists(save_res["env_path"])


def test_mcp_server_tool_handlers():
    from coolify_mcp_server import handle_tool_call, TOOLS
    assert len(TOOLS) >= 12

    # Call cluster status
    status = handle_tool_call("coolify_get_cluster_status", {})
    assert status["status"] in ("healthy", "degraded")

    # Call search templates
    ai_templates = handle_tool_call("coolify_search_templates", {"query": "llm"})
    assert len(ai_templates) > 0

    # Call export compose
    compose_data = handle_tool_call("coolify_export_compose", {"template_id": "anythingllm"})
    assert "docker_compose_yaml" in compose_data
    assert "generated_env" in compose_data


def test_orchestrator_do_everything(orchestrator):
    manifest = orchestrator.do_everything()
    assert manifest["status"] == "SOVEREIGN PAAS FULL POWERS VERIFIED"
    assert manifest["total_phases_executed"] == 8
    assert manifest["resources"]["nodes"] >= 2
    assert manifest["resources"]["projects"] >= 3
    assert manifest["resources"]["databases"] >= 4
    assert manifest["resources"]["services"] >= 4
    assert manifest["resources"]["applications"] >= 2
    assert manifest["resources"]["catalog_templates"] >= 350
    assert os.path.exists("omega/data/coolify_do_everything_manifest.json")


def test_cli_do_everything(orchestrator, capsys):
    class Args:
        server = "srv-localhost-000"
    coolify_cli.cmd_do_everything(orchestrator, Args())
    out = capsys.readouterr().out
    assert "COOLIFY v4" in out
    assert "SOVEREIGN PAAS FULL POWERS VERIFIED" in out
    assert "PHASES EXECUTED" in out
    assert "FINAL CLUSTER HEALTH" in out


def test_mcp_do_everything():
    from coolify_mcp_server import handle_tool_call, TOOLS
    assert any(t["name"] == "coolify_do_everything" for t in TOOLS)

    res = handle_tool_call("coolify_do_everything", {"server_uuid": "srv-localhost-000"})
    assert res["status"] == "SOVEREIGN PAAS FULL POWERS VERIFIED"
    assert len(res["phases"]) == 8

