import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    assert client.get("/health").json == {"status": "healthy"}


def test_chat(client):
    result = client.post("/api/chat", json={"message": "How do I manage my budget?"})
    assert result.status_code == 200
    assert "tracking" in result.json["response"]


@pytest.mark.parametrize("payload", [{"message": ""}, {"message": "  "}])
def test_empty(client, payload):
    assert client.post("/api/chat", json=payload).status_code == 400


def test_missing(client):
    assert client.post("/api/chat", json={}).status_code == 400


def test_invalid_json(client):
    assert client.post("/api/chat", data="{bad", content_type="application/json").status_code == 400


def test_too_long(client):
    assert client.post("/api/chat", json={"message": "a" * 1001}).status_code == 400


@pytest.mark.parametrize("value", [123, [], None, {"a": 1}])
def test_invalid_type(client, value):
    assert client.post("/api/chat", json={"message": value}).status_code == 400


def test_invalid_body_type(client):
    assert client.post("/api/chat", json=["hello"]).status_code == 400


def test_non_json(client):
    assert client.post("/api/chat", data="message=hello").status_code == 415
