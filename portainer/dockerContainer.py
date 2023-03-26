"""Class to interact with Portainer docker containers."""
from __future__ import annotations

from .const import (
    API_IMAGE_STATUS,
    API_STATS,
    API_RECREATE,
)
from .exceptions import (PortainerException)

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portainer import Portainer

class PortainerDockerContainer():
    """Portainer docker containers class."""

    def __init__(self, portainer: Portainer, endpointId: str, dockerContainer: dict) -> None:
        self._portainer = portainer
        self._endpointId = endpointId
        self.afterRefresh(dockerContainer)

    def afterRefresh(self, dockerContainer : dict) -> None:
        self._id = dockerContainer["Id"]
        self._name = dockerContainer["Names"][0][1:]
        self._image = dockerContainer["Image"]
        self._imageId = dockerContainer["ImageID"]
        self._state = dockerContainer["State"]
        self._status = dockerContainer["Status"]
        self._created = dockerContainer["Created"]
    
    async def getImageStatus(self) -> dict:
        api = API_IMAGE_STATUS.format(self._endpointId, self._id)
        response = await self._portainer.runCommand("GET", api, None)
        
        if response.status_code == 200:
            image_status = json.loads(response.text)
            self._image_status = image_status["Status"]
            return image_status
        else:
            data = json.loads(response.text)
            raise PortainerException(api, response.status_code, data["message"], data["details"])
    
    async def getStats(self) -> dict:
        api = API_STATS.format(self._endpointId, self._id)
        api += "?stream=false"
        response = await self._portainer.runCommand("GET", api, None)
        
        if response.status_code == 200:
            stats = json.loads(response.text)
            self._stas = stats
            return stats
        else:
            data = json.loads(response.text)
            raise PortainerException(api, response.status_code, data["message"], data["details"])
        
    async def recreate(self, pullImage = True) -> dict:
        api = API_RECREATE.format(self._endpointId, self._id)
        param = {
            "PullImage": pullImage
        }
        response = await self._portainer.runCommand("POST", api, param)
        
        if response.status_code == 200:
            container = json.loads(response.text)
            self._id = container["Id"]
            self._id = container["State"]["Status"]
            return container
        else:
            data = json.loads(response.text)
            raise PortainerException(api, response.status_code, data["message"], data["details"])
