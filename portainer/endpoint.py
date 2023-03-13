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
        self._dockerContainer = {}
        self.afterRefresh(endpoint)

    async def refresh(self) -> None:
        response = await self._portainer.runCommand(API_ENDPOINT)
        if response.status_code == 200:
            ret = []
            endpoints = json.loads(response.text)
            for endpoint in endpoints:
                ret.append(PortainerEndpoint(self, endpoint))
        else:
            data = json.loads(response.text)
            raise PortainerException(API_ENDPOINT, response.status_code, data["message"], data["details"])

    def afterRefresh(self, endpoint : dict) -> None:
        self._id = endpoint["Id"]
        self._name = endpoint["Name"]
        self._type = endpoint["Type"]
        self._URL = endpoint["URL"]
        self._groupId = endpoint["GroupId"]
        self._publicURL = endpoint["PublicURL"]
        self._status = endpoint["Status"]
        self.generateContainers(endpoint["Snapshots"][0]["DockerSnapshotRaw"]["Containers"])

    def generateContainers(self, containers : dict) -> None:
        for container in containers:
            if container["Names"][0][1:] in self._dockerContainer:
                self._dockerContainer[container["Names"][0][1:]].afterRefresh(container)
            else:
                self._dockerContainer[container["Names"][0][1:]] = PortainerDockerContainer(self._portainer, self._id, container)
