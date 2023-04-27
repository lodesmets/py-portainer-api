"""Class to interact with Portainer endpoints."""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict

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
        self.docker_container: Dict[str, PortainerDockerContainer] = {}
        self.after_refresh(endpoint)

    async def refresh(self) -> None:
        """Refresh properties."""
        api = API_ENDPOINT.format(environment_id=self.endpoint_id)
        response = await self._portainer.get(api, None)
        if response["status_code"] == 200:
            self.after_refresh(response["body"])
        else:
            raise PortainerException(
                api,
                response["status_code"],
                response["body"]["message"],
                response["body"]["details"],
            )

    def after_refresh(self, endpoint: dict) -> None:
        """Set variables from a refresh."""
        self.endpoint_id = endpoint["Id"]
        self.name = endpoint["Name"]
        self.type = endpoint["Type"]
        self.url = endpoint["URL"]
        self.group_id = endpoint["GroupId"]
        self.public_url = endpoint["PublicURL"]
        self.status = endpoint["Status"]
        self.status_message = endpoint["StatusMessage"]
        self.time = endpoint["QueryDate"]
        self.generate_containers(
            endpoint["Snapshots"][0]["DockerSnapshotRaw"]["Containers"]
        )

    def generate_containers(self, containers: dict) -> None:
        """Create or update container objects."""
        for container in containers:
            if container["Names"][0][1:] in self.docker_container:
                self.docker_container[container["Names"][0][1:]].after_refresh(
                    container
                )
            else:
                self.docker_container[
                    container["Names"][0][1:]
                ] = PortainerDockerContainer(
                    self._portainer, self.endpoint_id, container
                )
