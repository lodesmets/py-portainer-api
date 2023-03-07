"""Class to interact with Portainer endpoints."""
from __future__ import annotations

from typing import TYPE_CHECKING

from dockerContainer import PortainerDockerContainer

if TYPE_CHECKING:
    from portainer import Portainer

class PortainerEndpoint():
    """Portainer endpoints class."""

    def __init__(self, portainer: Portainer) -> None:
        """Constructor method."""
        self._portainer = portainer
        
    
    def afterRefresh(self, endpoint : dict) -> None:
        self._id = endpoint.Id
        self._name = endpoint.Name
        self._type = endpoint.Type
        self._URL = endpoint.URL
        self._groupId = endpoint.GroupId
        self._publicURL = endpoint.PublicURL
        self._status = endpoint.Status

        self._dockerContainer = []
        
        endpoints = json.loads(response.text)


