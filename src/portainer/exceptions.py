"""Library exceptions."""


class PortainerException(Exception):
    """Generic Portainer exception."""

    def __init__(
        self,
        api: str | None,
        code: int,
        message: str | None = None,
        details: str | None = None,
    ) -> None:
        """Constructor method."""
        error_message = {
            "api": api,
            "code": code,
            "message": message,
            "details": details,
        }
        super().__init__(error_message)


class PortainerNotLoggedInException(PortainerException):
    """Not logged in exception."""

    def __init__(self) -> None:
        """Constructor method."""
        super().__init__(None, -1, "Not logged in. You have to do login() first.", "")


class PortainerRequestException(PortainerException):
    """Request exception."""

    def __init__(self, exception: Exception) -> None:
        """Constructor method."""
        ex_class = exception.__class__.__name__
        if not exception.args:
            super().__init__(None, -1, None, ex_class)
            return
        ex_reason = exception.args[0]
        if hasattr(exception.args[0], "reason"):
            ex_reason = exception.args[0].reason
        super().__init__(None, -1, f"{ex_class} = {ex_reason}")
