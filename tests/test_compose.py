"""
Tests for docker-compose.yml structure.
Validates services, networks, ports, healthchecks, and build contexts.
"""
import os
import pytest
import yaml

COMPOSE_PATH = os.path.join(os.path.dirname(__file__), "..", "docker-compose.yml")
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="module")
def compose():
    with open(COMPOSE_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def services(compose):
    return compose["services"]


@pytest.fixture(scope="module")
def networks(compose):
    return compose.get("networks", {})


# ── Наличие сервисов ──────────────────────────────────────────────────────────

def test_python_app_service_exists(services):
    assert "python-app" in services


def test_go_info_service_exists(services):
    assert "go-info" in services


def test_rust_textutil_service_exists(services):
    assert "rust-textutil" in services


# ── Сеть ─────────────────────────────────────────────────────────────────────

def test_network_lab11_net_exists(networks):
    assert "lab11-net" in networks


def test_network_lab11_net_driver_bridge(networks):
    assert networks["lab11-net"]["driver"] == "bridge"


def test_python_app_uses_lab11_net(services):
    nets = services["python-app"]["networks"]
    assert "lab11-net" in nets


def test_go_info_uses_lab11_net(services):
    nets = services["go-info"]["networks"]
    assert "lab11-net" in nets


def test_rust_textutil_uses_lab11_net(services):
    nets = services["rust-textutil"]["networks"]
    assert "lab11-net" in nets


# ── Порты ─────────────────────────────────────────────────────────────────────

def test_python_app_port_5005(services):
    ports = services["python-app"]["ports"]
    assert any("5005" in str(p) for p in ports)


def test_go_info_port_8080(services):
    ports = services["go-info"]["ports"]
    assert any("8080" in str(p) for p in ports)


# ── Healthcheck ───────────────────────────────────────────────────────────────

def test_python_app_has_healthcheck(services):
    assert "healthcheck" in services["python-app"]


def test_go_info_has_healthcheck(services):
    assert "healthcheck" in services["go-info"]


def test_python_app_healthcheck_has_test(services):
    hc = services["python-app"]["healthcheck"]
    assert "test" in hc and len(hc["test"]) > 0


def test_go_info_healthcheck_has_test(services):
    hc = services["go-info"]["healthcheck"]
    assert "test" in hc and len(hc["test"]) > 0


def test_python_app_healthcheck_has_interval(services):
    assert "interval" in services["python-app"]["healthcheck"]


def test_go_info_healthcheck_has_interval(services):
    assert "interval" in services["go-info"]["healthcheck"]


# ── Restart policy ────────────────────────────────────────────────────────────

def test_python_app_restart_unless_stopped(services):
    assert services["python-app"]["restart"] == "unless-stopped"


def test_go_info_restart_unless_stopped(services):
    assert services["go-info"]["restart"] == "unless-stopped"


def test_rust_textutil_restart_no(services):
    assert services["rust-textutil"]["restart"] == "no"


# ── Build contexts ────────────────────────────────────────────────────────────

def test_python_app_build_context_exists(services):
    ctx = services["python-app"]["build"]
    path = os.path.join(REPO_ROOT, ctx.lstrip("./"))
    assert os.path.isdir(path), f"Build context not found: {path}"


def test_go_info_build_context_exists(services):
    ctx = services["go-info"]["build"]
    path = os.path.join(REPO_ROOT, ctx.lstrip("./"))
    assert os.path.isdir(path), f"Build context not found: {path}"


def test_rust_textutil_build_context_exists(services):
    ctx = services["rust-textutil"]["build"]
    path = os.path.join(REPO_ROOT, ctx.lstrip("./"))
    assert os.path.isdir(path), f"Build context not found: {path}"


# ── Environment ───────────────────────────────────────────────────────────────

def test_go_info_has_environment(services):
    assert "environment" in services["go-info"]


def test_go_info_environment_port_8080(services):
    env = services["go-info"]["environment"]
    # environment может быть списком строк или словарём
    if isinstance(env, list):
        assert "PORT=8080" in env
    else:
        assert env.get("PORT") == 8080 or str(env.get("PORT")) == "8080"


# ── Command ───────────────────────────────────────────────────────────────────

def test_rust_textutil_has_command(services):
    assert "command" in services["rust-textutil"]


def test_rust_textutil_command_starts_with_count(services):
    cmd = services["rust-textutil"]["command"]
    assert cmd[0] == "count"
