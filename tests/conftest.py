import pytest

from app import create_app
from app.repositories.event_repository import InMemoryEventRepository


@pytest.fixture
def repo():
    return InMemoryEventRepository()


@pytest.fixture
def app(repo):
    return create_app({"TESTING": True, "WTF_CSRF_ENABLED": False}, repository=repo)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def service(app):
    return app.extensions["event_service"]   # the app's own service, so the pages see what the tests create
