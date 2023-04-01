"""Class to interact with Portainer endpoints."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING

from .const import API_ENDPOINT
from .docker_container import PortainerDockerContainer
from .exceptions import PortainerException

if TYPE_CHECKING:
    from portainer import Portainer


class PortainerEndpoint:
    """Portainer endpoints class."""

    def __init__(self, portainer: Portainer, endpoint: dict) -> None:
        """Constructor method."""
        self._portainer = portainer
        self._docker_container: list[PortainerDockerContainer]
        self.after_refresh(endpoint)

    async def refresh(self) -> None:
        """Refresh properties."""
        api = API_ENDPOINT.format(self._id)
        response = await self._portainer.run_command("GET", api, None)
        if response.status_code == 200:
            endpoint = json.loads(response.text)
            self.after_refresh(endpoint)
        else:
            data = json.loads(response.text)
            raise PortainerException(
                api, response.status_code, data["message"], data["details"]
            )

    def after_refresh(self, endpoint: dict) -> None:
        """Set variables from a refresh."""
        self._id = endpoint["Id"]
        self._name = endpoint["Name"]
        self._type = endpoint["Type"]
        self._url = endpoint["URL"]
        self._group_id = endpoint["GroupId"]
        self._public_url = endpoint["PublicURL"]
        self._status = endpoint["Status"]
        self._time = endpoint["QueryDate"]
        self.generate_containers(
            endpoint["Snapshots"][0]["DockerSnapshotRaw"]["Containers"]
        )

    def generate_containers(self, containers: dict) -> None:
        """Create or update container objects."""
        for container in containers:
            if container["Names"][0][1:] in self._docker_container:
                self._docker_container[container["Names"][0][1:]].afterRefresh(
                    container
                )
            else:
                self._docker_container[
                    container["Names"][0][1:]
                ] = PortainerDockerContainer(self._portainer, self._id, container)
