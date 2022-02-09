from fastapi.testclient import TestClient

from handler.app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/heartbeat")
    assert response.status_code == 200
    assert response.json() == {"message": "Service Ok"}