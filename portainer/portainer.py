"""Class to interact with Portainer."""
import requests
import logging
import json
from .endpoint import PortainerEndpoint

from .const import (
    API_AUTH,
    API_ENDPOINTS,
)

from typing import List, Any, TypedDict

from .exceptions import (PortainerException)
    

_LOGGER = logging.getLogger(__name__)

class Portainer:
    """Class containing the main Portainer functions."""

    def __init__(
        self,
        portainer_ip: str,
        portainer_port: int,
        username: str,
        password: str,
        use_https: bool = False,
        debugmode: bool = False,
    ):
        """Constructor method."""
        self._username = username
        self._password = password
        self._debugmode = debugmode

        # Login
        self._auth_token: str | None = None

        # Build variables
        if use_https:
            self._base_url = f"https://{portainer_ip}:{portainer_port}/api/"
        else:
            self._base_url = f"http://{portainer_ip}:{portainer_port}/api/"
    
    def _debuglog(self, message: str) -> None:
        """Outputs message if debug mode is enabled."""
        _LOGGER.debug(message)
        if self._debugmode:
            print("DEBUG: " + message)

    async def post(self, api : str, params : dict | None) :
        api_url = self._base_url + api
        headers = {"Authorization": f"Bearer {self._auth_token}"}
        return requests.post(api_url, headers = headers, json = params)
    
    async def get(self, api : str, params : dict | None) :
        api_url = self._base_url + api
        headers = {"Authorization": f"Bearer {self._auth_token}"}
        return requests.get(api_url, headers = headers, json = params)
    
    async def runCommand(self, method : str, api : str, params : dict | None, autoLogin : bool | True):
        self._debuglog("method: " + method + "api: " + api + "params: " + json.dumps(params))
        if method == "POST":
            response = await self.post(api, params)
        elif method == "GET":
            response = await self.get(api, params)
        if response.status_code == 401 and autoLogin: # not authorized, retry login
            if self.login():
                response = await self.runCommand(method, api, params, False)
        self._debuglog("Response status code: {}".format(response.status_code))
        return response

    async def login(self) -> bool:
        """Create a logged session."""
        # First reset the session
        self._debuglog("Creating new session")

        params = {
            "username": self._username,
            "password": self._password,
        }

        # Request login
        response = await self.post(API_AUTH, params)
        self._debuglog("Response status code: {}".format(response.status_code))
        if response.status_code == 200:
            self._auth_token = response.json()["jwt"]
            return True
        else:
            data = json.loads(response.text)
            raise PortainerException(API_AUTH, response.status_code, data["message"], data["details"])

    async def getEndpoints(self, start : int | None = None, limit : int| None = None, groupIds : List[int] | None = None, endpointIds : List[int] | None = None) -> List[PortainerEndpoint] | None :
        params = {}
        if start is not None:
            params["start"] = start
        if limit is not None:
            params["limit"] = limit
        if groupIds is not None:
            params["groupIds"] = groupIds
        if endpointIds is not None:
            params["endpointIds"] = endpointIds

        response = await self.runCommand("GET", API_ENDPOINTS, params)
        if response.status_code == 200:
            ret = []
            endpoints = json.loads(response.text)
            for endpoint in endpoints:
                ret.append(PortainerEndpoint(self, endpoint))
        else:
            data = json.loads(response.text)
            raise PortainerException(API_ENDPOINTS, response.status_code, data["message"], data["details"])
