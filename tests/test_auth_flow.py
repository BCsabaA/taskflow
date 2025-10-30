from app import create_app, db
from app.models import User

def test_register_login_logout(tmp_path, monkeypatch):
    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False  # teszt egyszerűsítés
    client = app.test_client()

    # Register
    res = client.post("/auth/register", data={"email":"a@b.c","password":"secret123"}, follow_redirects=True)
    assert res.status_code == 200
    with app.app_context():
        assert User.query.filter_by(email="a@b.c").first() is not None

    # Login
    res = client.post("/auth/login", data={"email":"a@b.c","password":"secret123"}, follow_redirects=True)
    assert res.status_code == 200
    assert b"Taskflow" in res.data

    # Logout
    res = client.get("/auth/logout", follow_redirects=True)
    assert res.status_code == 200
