"""Library tests."""
import re

from requests import Response


class PortainerMock:
    """Mocked Portainer."""

    async def run_command(
        self, method: str, api: str, params: dict | None, auto_login: bool = True
    ) -> Response:
        """Mocked run_command."""
        del method, params, auto_login
        arguments = re.findall(r"{(.*?)}", api)
        if "environment_id" in arguments:
            api = api.format(environment_id=1)
        if "container_id" in arguments:
            api = api.format(container_id=1)
        ret = Response()
        ret.status_code = 200
        return ret
