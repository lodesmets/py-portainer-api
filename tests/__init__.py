"""Library tests."""
from portainer import Portainer


class PortainerMock(Portainer):
    """Mocked Portainer."""

    def __init__(
        self,
        session,
        portainer_ip,
        portainer_port,
        username,
        password,
        timeout: int = 600,
        use_https: bool = False,
        debugmode: bool = False,
    ):
        """Constructor method."""
        Portainer.__init__(
            self,
            session,
            portainer_ip,
            portainer_port,
            username,
            password,
            timeout,
            use_https,
            debugmode,
        )

    async def _execute_request(
        self, method: str, url: str, params: dict | None, headers: dict | None = None
    ) -> dict:
        ret: dict[str, str | int] = {}
        ret["status_code"] = 200
        ret["body"] = "test"
        return ret
