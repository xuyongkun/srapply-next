import pytest


@pytest.fixture
def token(client):
    resp = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    return resp.json()["access_token"]


@pytest.fixture
def consult_token(client):
    resp = client.post("/api/auth/login", json={"username": "consultant", "password": "consult123"})
    return resp.json()["access_token"]


@pytest.fixture
def oper_token(client):
    resp = client.post("/api/auth/login", json={"username": "operator", "password": "oper123"})
    return resp.json()["access_token"]


@pytest.fixture
def lead_id(token, client):
    resp = client.post(
        "/api/chat/visitor",
        json={"visitor_id": "v-admin-test", "message": "hello", "page_url": "/"},
    )
    return resp.json()["lead_id"]


def test_list_leads_requires_auth(client):
    resp = client.get("/api/admin/leads")
    assert resp.status_code == 401


def test_list_leads_as_operator(oper_token, client):
    resp = client.get("/api/admin/leads", headers={"Authorization": f"Bearer {oper_token}"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_update_lead_status(token, lead_id, client):
    resp = client.patch(
        f"/api/admin/leads/{lead_id}/status",
        json={"status": "contacted"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200


def test_update_lead_invalid_status(token, lead_id, client):
    resp = client.patch(
        f"/api/admin/leads/{lead_id}/status",
        json={"status": "invalid_status"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 400


def test_update_lead_not_found(token, client):
    resp = client.patch(
        "/api/admin/leads/99999/status",
        json={"status": "contacted"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 404


def test_assign_lead(token, lead_id, client):
    resp = client.patch(
        f"/api/admin/leads/{lead_id}/assign",
        json={"assigned_to": "consultant"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200


def test_operator_cannot_assign(oper_token, lead_id, client):
    resp = client.patch(
        f"/api/admin/leads/{lead_id}/assign",
        json={"assigned_to": "someone"},
        headers={"Authorization": f"Bearer {oper_token}"},
    )
    assert resp.status_code == 403


def test_operator_cannot_update_status(oper_token, lead_id, client):
    resp = client.patch(
        f"/api/admin/leads/{lead_id}/status",
        json={"status": "done"},
        headers={"Authorization": f"Bearer {oper_token}"},
    )
    assert resp.status_code == 403


def test_list_lead_messages(token, lead_id, client):
    resp = client.get(
        f"/api/admin/leads/{lead_id}/messages",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    msgs = resp.json()
    assert len(msgs) >= 2  # user message + bot reply


def test_list_users(token, client):
    resp = client.get("/api/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    users = resp.json()
    assert len(users) == 3
    assert users[0]["username"] == "admin"
