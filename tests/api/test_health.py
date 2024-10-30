import pytest

def test_liveness(client):
    response = client.get("/health/liveness")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

@pytest.mark.asyncio
async def test_readiness(client):
    response = client.get("/health/readiness")
    assert response.status_code == 200
    assert response.json() == {"status": "ready", "database": "connected"} 