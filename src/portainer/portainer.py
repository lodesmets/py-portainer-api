"""Class to interact with Portainer."""
from __future__ import annotations

import asyncio
import logging
from json import JSONDecodeError
from typing import List, Union
from urllib.parse import quote, urlencode

import aiohttp
import async_timeout
from yarl import URL

from .const import API_AUTH, API_ENDPOINTS
from .endpoint import PortainerEndpoint
from .exceptions import (
    PortainerException,
    PortainerNotLoggedInException,
    PortainerRequestException,
)

_LOGGER = logging.getLogger(__name__)


class Portainer:
    """Class containing the main Portainer functions."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        portainer_ip: str,
        portainer_port: int,
        username: str,
        password: str,
        timeout: int = 600,
        use_https: bool = False,
        debugmode: bool = False,
    ):
        """Constructor method."""
        self._username = username
        self._password = password
        self._debugmode = debugmode

        self._timeout = timeout

        # Session
        self._session = session

        # Login
        self._auth_token: str | None = None

        # Build variables
        if use_https:
            self._base_url = f"https://{portainer_ip}:{portainer_port}/api"
        else:
            self._base_url = f"http://{portainer_ip}:{portainer_port}/api"

    def _debuglog(self, message: str) -> None:
        """Outputs message if debug mode is enabled."""
        _LOGGER.debug(message)
        if self._debugmode:
            print("DEBUG: " + message)

    async def post(self, api: str, params: dict | None = None) -> dict:
        """Handles API POST request."""
        return await self._request("POST", api, params)

    async def get(self, api: str, params: dict | None = None) -> dict:
        """Handles API GET request."""
        return await self._request("GET", api, params)

    async def _request(
        self,
        request_method: str,
        api: str,
        params: dict | None = None,
        retry_once: bool = True,
    ) -> dict:
        """Handles API request."""
        url, params, headers = await self._prepare_request(api, params)

        # Request data
        self._debuglog("API: " + api)
        self._debuglog("Request Method: " + request_method)
        response = await self._execute_request(request_method, url, params, headers)
        self._debuglog("Successful returned data")
        self._debuglog("RESPONSE: " + str(response))

        # Handle data errors
        if api != API_AUTH and response["status_code"] == 401 and retry_once:
            # Session ID is expired
            if self.login():
                response = await self._request(request_method, api, params, False)
        return response

    async def _prepare_request(
        self,
        api: str,
        params: dict | None = None,
    ) -> tuple[str, dict, dict | None]:
        """Prepare the url and parameters for a request."""
        # Check if logged
        if not self._auth_token and api not in [API_AUTH]:
            raise PortainerNotLoggedInException
        # Build request params
        if not params:
            params = {}
        headers = None
        if self._auth_token:
            headers = {"Authorization": f"Bearer {self._auth_token}"}
        url = f"{self._base_url}/{api}"
        return (url, params, headers)

    async def _execute_request(
        self, method: str, url: str, params: dict | None, headers: dict | None = None
    ) -> dict:
        """Function to execute and handle a request."""
        if params:
            # special handling for spaces in parameters
            # because yarl.URL does encode a space as + instead of %20
            # safe extracted from yarl.URL._QUERY_PART_QUOTER
            safe = "?/:@-._~!$'()*,"
            query = urlencode(params, safe=safe, quote_via=quote)
            url_encoded = URL(str(URL(url)) + "?" + query, encoded=True)
        else:
            url_encoded = URL(url)

        try:
            if method == "GET":
                async with async_timeout.timeout(self._timeout):
                    response = await self._session.get(url_encoded, headers=headers)
            elif method == "POST":
                self._debuglog("POST data: " + str(params))
                async with async_timeout.timeout(self._timeout):
                    response = await self._session.post(
                        url, json=params, headers=headers
                    )

            # mask sesitiv parameters
            response_url = response.url
            # for param in SENSITIV_PARAMS:
            #    if params is not None and params.get(param):
            #        response_url = response_url.update_query({param: "*********"})
            self._debuglog("Request url: " + str(response_url))
            self._debuglog("Response status_code: " + str(response.status))
            self._debuglog("Response headers: " + str(dict(response.headers)))

            content_type = response.headers.get("Content-Type", "").split(";")[0]
            ret: dict[str, str | int] = {}
            ret["status_code"] = response.status
            if content_type in [
                "application/json",
                "text/json",
            ]:
                ret["body"] = await response.json(content_type=content_type)
            else:
                ret["body"] = await response.text()
            return ret
        except (asyncio.TimeoutError, JSONDecodeError) as exp:
            raise PortainerRequestException(exp) from exp

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
        if response["status_code"] == 200:
            self._auth_token = response["body"]["jwt"]
            return True

        if isinstance(response["body"], dict):
            raise PortainerException(
                API_AUTH,
                response["status_code"],
                response["body"]["message"],
                response["body"]["details"],
            )
        raise PortainerException(API_AUTH, response["status_code"], response["body"])

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

        response = await self.get(API_ENDPOINTS, params)
        if response["status_code"] == 200:
            ret = []
            endpoints = response["body"]
            for endpoint in endpoints:
                ret.append(PortainerEndpoint(self, endpoint))
            return ret
        raise PortainerException(
            API_ENDPOINTS,
            response["status_code"],
            response["body"]["message"],
            response["body"]["details"],
        )
