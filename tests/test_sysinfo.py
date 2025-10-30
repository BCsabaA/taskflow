from app import create_app


def test_about_has_versions():
    app = create_app()
    client = app.test_client()
    res = client.get("about")
    assert res.status_code == 200
    html = res.data.decode("utf-8").lower()
    assert "python" in html
    assert "flask" in html
    assert "sqlite" in html