from app import create_app

def test_index_ok():
    app = create_app()
    client = app.test_client()

    res = client.get("/")

    assert res.status_code == 200
    assert b"Hello" in res.data