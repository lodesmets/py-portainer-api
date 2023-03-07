"""Library exceptions."""

class PortainerException(Exception):
    """Generic Portainer exception."""

    def __init__(self, api: str | None, code: int, message: str, details : str) -> None:
        """Constructor method."""
        error_message = {"api": api, "code": code, "message": message, "details": details}
        super().__init__(error_message)