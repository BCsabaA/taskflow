from app import create_app
from app.models import User, UserSettings
from werkzeug.security import generate_password_hash

def test_update_settings():
    app = create_app()
    app.config["WTF_CSRF_ENABLED"] = False
    client = app.test_client()

    with app.app_context():
        u = User(email="u@test.tld", password_hash=generate_password_hash("pw123456"))
        from app import db
        db.session.add(u); db.session.flush()
        s = UserSettings(user_id=u.id)
        db.session.add(s); db.session.commit()

    # login
    client.post("/auth/login", data={"email":"u@test.tld","password":"pw123456"}, follow_redirects=True)

    # update settings
    res = client.post("/auth/settings", data={
        "default_list_id": "1",
        "default_priority": "3",
        "default_status": "DOING",
        "default_due_days": "2",
        "quick_add_fields": '["title","list_id"]'
    }, follow_redirects=True)
    assert res.status_code == 200

    with app.app_context():
        s = UserSettings.query.filter_by(user_id=1).first()
        assert s.default_list_id == 1
        assert s.default_priority == 3
        assert s.default_status == "DOING"
        assert s.default_due_days == 2
        assert s.quick_add_fields is not None
