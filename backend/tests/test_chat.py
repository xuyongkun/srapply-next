def test_visitor_chat_creates_lead(client):
    resp = client.post(
        "/api/chat/visitor",
        json={
            "visitor_id": "v-test-1",
            "message": "我想申请美国研究生",
            "page_url": "http://localhost:5173/",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "reply" in data
    assert data["lead_id"] > 0
    assert data["notified_wechat"] is False  # no webhook configured


def test_visitor_chat_updates_lead(client):
    vid = "v-test-repeat"
    # first message creates lead
    r1 = client.post("/api/chat/visitor", json={"visitor_id": vid, "message": "hello"})
    lid1 = r1.json()["lead_id"]
    # second message updates same lead
    r2 = client.post("/api/chat/visitor", json={"visitor_id": vid, "message": "关于费用"})
    lid2 = r2.json()["lead_id"]
    assert lid1 == lid2


def test_visitor_chat_empty_message(client):
    resp = client.post("/api/chat/visitor", json={"visitor_id": "v-x", "message": ""})
    assert resp.status_code == 422


def test_rule_reply_contains_keywords(client):
    resp = client.post("/api/chat/visitor", json={"visitor_id": "v-kw", "message": "我想申请美国"})
    data = resp.json()
    assert "留学方向" in data["reply"] or "初步评估" in data["reply"]
