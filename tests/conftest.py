import pytest

from app import create_app
from app.ai.fake_ai_provider import FakeAIProvider
from app.repositories.in_memory_event_repository import InMemoryEventRepository


@pytest.fixture
def repo():
    return InMemoryEventRepository()


@pytest.fixture
def ai():
    return FakeAIProvider()   # tests never make a paid call


@pytest.fixture
def app(repo, ai):
    return create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    }, repository=repo, ai_provider=ai)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def service(app):
    return app.extensions["event_service"]   # the app's own service, so the pages see what the tests create
