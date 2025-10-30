from app import create_app

def test_healthcheck_ok():
    app = create_app()
    client = app.test_client()
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.is_json
    data = res.get_json()
    assert data["status"] == "ok"