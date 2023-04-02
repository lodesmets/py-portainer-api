"""Main conftest."""
import pytest

from portainer import Portainer


@pytest.fixture
def api() -> Portainer:
    """Return a mock portainer API."""
    return Portainer("192.168.0.1", 9000, "admin", "password")
