import pytest


@pytest.fixture
def token(client):
    resp = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    return resp.json()["access_token"]


def test_track_event(client):
    resp = client.post(
        "/api/analytics/track",
        json={"visitor_id": "v-a1", "event_type": "page_view", "page_url": "/"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


def test_track_event_with_payload(client):
    resp = client.post(
        "/api/analytics/track",
        json={
            "visitor_id": "v-a2",
            "event_type": "click",
            "page_url": "/about",
            "payload": '{"button":"apply"}',
        },
    )
    assert resp.status_code == 200


def test_summary_requires_auth(client):
    resp = client.get("/api/analytics/summary")
    assert resp.status_code == 401


def test_summary(token, client):
    # seed some data
    client.post("/api/analytics/track", json={"visitor_id": "v-sum1", "event_type": "page_view", "page_url": "/"})
    client.post("/api/chat/visitor", json={"visitor_id": "v-sum2", "message": "hello"})

    resp = client.get("/api/analytics/summary", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert "total_visitors" in data
    assert "consultation_visitors" in data
    assert "conversion_rate" in data
    assert isinstance(data["top_pages"], list)
