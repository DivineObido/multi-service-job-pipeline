import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_redis():
    with patch('main.r') as mock_r:
        yield mock_r


def test_create_job_returns_job_id(mock_redis):
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response = client.post("/jobs")

    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert len(data["job_id"]) > 0


def test_get_job_returns_status(mock_redis):
    mock_redis.hget.return_value = b"queued"

    response = client.get("/jobs/test-job-123")

    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "test-job-123"
    assert data["status"] == "queued"


def test_get_job_not_found(mock_redis):
    mock_redis.hget.return_value = None

    response = client.get("/jobs/nonexistent-job")

    assert response.status_code == 404


def test_create_job_pushes_to_redis(mock_redis):
    mock_redis.lpush.return_value = 1
    mock_redis.hset.return_value = 1

    response = client.post("/jobs")

    assert response.status_code == 200
    mock_redis.lpush.assert_called_once()
    mock_redis.hset.assert_called_once()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}