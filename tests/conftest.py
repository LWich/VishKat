from collections.abc import Iterator

import pytest
from app.container import Container
from app.main import create_app
from fastapi.testclient import TestClient


@pytest.fixture
def container() -> Iterator[Container]:
    instance = Container()
    yield instance
    instance.unwire()
    instance.shutdown_resources()


@pytest.fixture
def client(container: Container) -> TestClient:
    return TestClient(create_app(container))
