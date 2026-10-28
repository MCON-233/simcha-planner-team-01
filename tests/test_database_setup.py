from app.db import db


def test_tests_use_an_in_memory_database(app):
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_the_events_table_exists(app):
    with app.app_context():
        assert db.inspect(db.engine).has_table("events")
