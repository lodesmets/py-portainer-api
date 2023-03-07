"""Class to interact with Portainer docker containers."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portainer import Portainer

class PortainerDockerContainer():
    """Portainer docker containers class."""

    def __init__(self, portainer: Portainer, endpointId: str, dockerContainer: dict) -> None:
        self._portainer = portainer
        self._endpointId = endpointId