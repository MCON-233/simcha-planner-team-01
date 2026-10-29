from app import create_app


def test_create_app_reads_settings_from_dotenv(monkeypatch):
    seen = []
    monkeypatch.setattr("app.load_dotenv", lambda: seen.append(True))

    create_app({"TESTING": True})

    assert seen == [True]
