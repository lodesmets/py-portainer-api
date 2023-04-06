"""Class to interact with Portainer docker containers."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from .const import (
    API_CONTAINER_RESTART,
    API_CONTAINER_START,
    API_CONTAINER_STOP,
    API_IMAGE_STATUS,
    API_RECREATE,
    API_STATS,
)
from .exceptions import PortainerException

if TYPE_CHECKING:
    from portainer import Portainer


class PortainerDockerContainer:
    """Portainer docker containers class."""

    def __init__(
        self, portainer: Portainer, endpoint_id: str, docker_container: dict
    ) -> None:
        """Constructor method."""
        self._portainer = portainer
        self._endpoint_id = endpoint_id
        self.image_status = ""
        self.container_id = ""
        self.status = ""
        self.stats: dict[Any, Any] = {}
        self.after_refresh(docker_container)

    def after_refresh(self, docker_container: dict) -> None:
        """Sets all variables."""
        self.container_id = docker_container["Id"]
        self.name = docker_container["Names"][0][1:]
        self.image = docker_container["Image"]
        self.image_id = docker_container["ImageID"]
        self.state = docker_container["State"]
        self.status = docker_container["Status"]
        self.created = docker_container["Created"]

    async def get_image_status(self) -> dict:
        """Request the status of the container."""
        api = API_IMAGE_STATUS.format(
            environment_id=self._endpoint_id, container_id=self.container_id
        )
        response = await self._portainer.run_command("GET", api, None)

        if response.status_code == 200:
            image_status = {}
            image_status = json.loads(response.text)
            self.image_status = image_status["Status"]
            return image_status
        data = json.loads(response.text)
        raise PortainerException(
            api, response.status_code, data["message"], data["details"]
        )

    async def get_stats(self) -> dict:
        """Request the stats of the container."""
        api = API_STATS.format(
            environment_id=self._endpoint_id, container_id=self.container_id
        )
        api += "?stream=false"
        response = await self._portainer.run_command("GET", api, None)

        if response.status_code == 200:
            stats = {}
            stats = json.loads(response.text)
            self.stats = stats
            return stats

        data = json.loads(response.text)
        raise PortainerException(
            api, response.status_code, data["message"], data["details"]
        )

    async def recreate(self, pull_image: bool = True) -> dict:
        """Recreate the container."""
        api = API_RECREATE.format(
            environment_id=self._endpoint_id, container_id=self.container_id
        )
        param = {"PullImage": pull_image}
        response = await self._portainer.run_command("POST", api, param)

        if response.status_code == 200:
            container = {}
            container = json.loads(response.text)
            self.container_id = container["Id"]
            self.status = container["State"]["Status"]
            return container
        data = json.loads(response.text)
        raise PortainerException(
            api, response.status_code, data["message"], data["details"]
        )

    async def stop(self) -> None:
        """Stop the container."""
        api = API_CONTAINER_STOP.format(
            environment_id=self._endpoint_id, container_id=self.container_id
        )
        response = await self._portainer.run_command("POST", api, None)
        if response.status_code != 204:
            data = json.loads(response.text)
            raise PortainerException(api, response.status_code, data["message"], "")

    async def start(self) -> None:
        """Start the container."""
        api = API_CONTAINER_START.format(
            environment_id=self._endpoint_id, container_id=self.container_id
        )
        response = await self._portainer.run_command("POST", api, None)
        if response.status_code != 204:
            data = json.loads(response.text)
            raise PortainerException(api, response.status_code, data["message"], "")

    async def restart(self) -> None:
        """Restart the container."""
        api = API_CONTAINER_RESTART.format(
            environment_id=self._endpoint_id, container_id=self.container_id
        )
        response = await self._portainer.run_command("POST", api, None)
        if response.status_code != 204:
            data = json.loads(response.text)
            raise PortainerException(api, response.status_code, data["message"], "")
