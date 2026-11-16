import pytest
from flask.testing import FlaskClient

from app import create_app


@pytest.fixture()
def client() -> FlaskClient:
    app = create_app({"TESTING": True})
    return app.test_client()


def test_health(client: FlaskClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
