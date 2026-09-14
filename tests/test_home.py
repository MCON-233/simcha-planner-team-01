import pytest
from flask.testing import FlaskClient

from app import create_app


@pytest.fixture()
def client() -> FlaskClient:
    app = create_app({"TESTING": True})
    return app.test_client()


def test_home_page_returns_ok(client: FlaskClient) -> None:
    response = client.get("/")

    assert response.status_code == 200


def test_home_page_has_header_main_and_footer(client: FlaskClient) -> None:
    html = client.get("/").get_data(as_text=True)

    assert 'href="#main-content"' in html
    assert '<header class="site-header">' in html
    assert '<nav aria-label="Primary">' in html
    assert '<main id="main-content"' in html
    assert '<footer class="site-footer">' in html


def test_home_page_has_content_sections(client: FlaskClient) -> None:
    html = client.get("/").get_data(as_text=True)

    assert "<h1" in html
    assert "Start Planning" in html
    for section_id in ("features", "simchas", "get-started"):
        assert f'id="{section_id}"' in html
