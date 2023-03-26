"""Class to interact with Portainer endpoints."""
from __future__ import annotations

from typing import TYPE_CHECKING
import json

from .const import (
    API_ENDPOINT,
)

from .dockerContainer import PortainerDockerContainer
from .exceptions import (PortainerException)

if TYPE_CHECKING:
    from portainer import Portainer

class PortainerEndpoint():
    """Portainer endpoints class."""

    def __init__(self, portainer: Portainer, endpoint: dict) -> None:
        """Constructor method."""
        self._portainer = portainer
        self._dockerContainer : list(PortainerDockerContainer) = {}
        self.afterRefresh(endpoint)

    async def refresh(self) -> None:
        api = API_ENDPOINT.format(self._id)
        response = await self._portainer.runCommand("GET", api, None)
        if response.status_code == 200:
            endpoint = json.loads(response.text)
            self.afterRefresh(endpoint)
        else:
            data = json.loads(response.text)
            raise PortainerException(api, response.status_code, data["message"], data["details"])

    def afterRefresh(self, endpoint : dict) -> None:
        self._id = endpoint["Id"]
        self._name = endpoint["Name"]
        self._type = endpoint["Type"]
        self._URL = endpoint["URL"]
        self._groupId = endpoint["GroupId"]
        self._publicURL = endpoint["PublicURL"]
        self._status = endpoint["Status"]
        self._time = endpoint["QueryDate"]
        self.generateContainers(endpoint["Snapshots"][0]["DockerSnapshotRaw"]["Containers"])

    def generateContainers(self, containers : dict) -> None:
        for container in containers:
            if container["Names"][0][1:] in self._dockerContainer:
                self._dockerContainer[container["Names"][0][1:]].afterRefresh(container)
            else:
                self._dockerContainer[container["Names"][0][1:]] = PortainerDockerContainer(self._portainer, self._id, container)
