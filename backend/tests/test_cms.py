import pytest


@pytest.fixture
def token(client):
    resp = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    return resp.json()["access_token"]


def test_list_cases_public(client):
    resp = client.get("/api/cms/cases")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_create_case(token, client):
    resp = client.post(
        "/api/cms/cases",
        json={"title": "Test Case", "summary": "A test case summary", "country": "USA", "major": "CS"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Test Case"
    assert data["id"] > 0


def test_create_case_requires_auth(client):
    resp = client.post(
        "/api/cms/cases",
        json={"title": "X", "summary": "Y", "country": "Z", "major": "W"},
    )
    assert resp.status_code == 401


def test_list_advisors_public(client):
    resp = client.get("/api/cms/advisors")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_create_advisor(token, client):
    resp = client.post(
        "/api/cms/advisors",
        json={"name": "张三", "title": "资深顾问", "bio": "十年留学咨询经验", "specialties": "美国,英国"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "张三"
    assert data["id"] > 0
