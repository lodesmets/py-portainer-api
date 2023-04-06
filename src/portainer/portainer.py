"""Class to interact with Portainer."""
from __future__ import annotations

import json
import logging
from typing import List, Union

import requests
from requests import Response

from .const import API_AUTH, API_ENDPOINTS
from .endpoint import PortainerEndpoint
from .exceptions import PortainerException

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

    async def post(self, api: str, params: dict | None) -> Response:
        """Handles API POST request."""
        api_url = self._base_url + api
        headers = {"Authorization": f"Bearer {self._auth_token}"}
        return requests.post(api_url, headers=headers, json=params, timeout=600)

    async def get(self, api: str, params: dict | None) -> Response:
        """Handles API GET request."""
        api_url = self._base_url + api
        headers = {"Authorization": f"Bearer {self._auth_token}"}
        return requests.get(api_url, headers=headers, json=params, timeout=600)

    async def run_command(
        self, method: str, api: str, params: dict | None, auto_login: bool = True
    ) -> Response:
        """Run command."""
        self._debuglog(
            "method: " + method + "api: " + api + "params: " + json.dumps(params)
        )
        if method == "POST":
            response = await self.post(api, params)
        elif method == "GET":
            response = await self.get(api, params)
        if response.status_code == 401 and auto_login:  # not authorized, retry login
            if self.login():
                response = await self.run_command(method, api, params, False)
        self._debuglog(f"Response status code: {response.status_code}")
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
        self._debuglog(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            self._auth_token = response.json()["jwt"]
            return True
        data = json.loads(response.text)
        raise PortainerException(
            API_AUTH, response.status_code, data["message"], data["details"]
        )

    async def get_endpoints(
        self,
        start: int | None = None,
        limit: int | None = None,
        group_ids: List[int] | None = None,
        endpoint_ids: List[int] | None = None,
    ) -> List[PortainerEndpoint] | None:
        """Get endpoints."""
        params: dict[str, Union[int, list[int]]] = {}
        if start is not None:
            params["start"] = start
        if limit is not None:
            params["limit"] = limit
        if group_ids is not None:
            params["groupIds"] = group_ids
        if endpoint_ids is not None:
            params["endpointIds"] = endpoint_ids

        response = await self.run_command("GET", API_ENDPOINTS, params)
        if response.status_code == 200:
            ret = []
            endpoints = json.loads(response.text)
            for endpoint in endpoints:
                ret.append(PortainerEndpoint(self, endpoint))
            return ret
        data = json.loads(response.text)
        raise PortainerException(
            API_ENDPOINTS, response.status_code, data["message"], data["details"]
        )
