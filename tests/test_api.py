"""
API Tests for GlobalScope MultiFrame 11.0
This file contains tests for the API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main_app import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/system/")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "message" in response.json()

def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health/")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "timestamp" in response.json()

def test_invalid_system_mode():
    """Test setting an invalid system mode."""
    response = client.post("/system/mode/INVALID")
    assert response.status_code == 200
    assert response.json()["status"] == "error"

def test_auth_login():
    """Test user login."""
    response = client.post("/auth/login", json={
        "username": "SuperHoloMisha",
        "token": "super_token"
    })
    assert response.status_code == 200

def test_auth_logout():
    """Test user logout."""
    response = client.post("/auth/logout", json={
        "session_id": "session_SuperHoloMisha_123"
    })
    assert response.status_code == 200

def test_chip_process():
    """Test creating a chip process."""
    response = client.post("/chip/process", json={
        "process_id": "test_process",
        "chip_data": {
            "type": "quantum_chip",
            "params": {
                "cores": 4,
                "frequency": 3.5
            }
        }
    })
    assert response.status_code == 200

def test_zero_defect():
    """Test zero defect engine."""
    response = client.post("/chip/zero-defect", json={
        "user_id": "SuperHoloMisha",
        "chip_id": "test_chip",
        "chip_data": {
            "type": "quantum_chip",
            "params": {
                "cores": 4,
                "frequency": 3.5
            }
        },
        "lang": "uk"
    })
    assert response.status_code == 200

def test_chip_metrics():
    """Test getting chip metrics."""
    response = client.get("/analytics/metrics/test_chip")
    assert response.status_code == 200

def test_chip_trends():
    """Test getting chip trends."""
    response = client.get("/analytics/trends/test_chip?hours=24")
    assert response.status_code == 200

def test_security_threats():
    """Test getting security threats."""
    response = client.get("/security/threats")
    assert response.status_code == 200

def test_rtl_hash():
    """Test generating RTL hash."""
    response = client.post("/hash/rtl", json={
        "rtl_code": "module example; endmodule",
        "algorithm": "sha256"
    })
    assert response.status_code == 200

def test_quantum_simulation():
    """Test running quantum simulation."""
    response = client.post("/simulate/quantum/test_chip", json={
        "sim_type": "OPTIMIZATION",
        "params": {
            "qubits": 10
        }
    })
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__])