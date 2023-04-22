"""Main conftest."""
import pytest

from portainer import Portainer

from . import PortainerMock


@pytest.fixture
def api() -> Portainer:
    """Return a mock portainer API."""
    return PortainerMock(None, "192.168.0.1", 9000, "admin", "password")
