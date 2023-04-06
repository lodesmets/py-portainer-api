"""Library constants."""
from typing import Final

# APIs
API_AUTH: Final = "auth"
API_ENDPOINTS: Final = "endpoints"
API_ENDPOINT: Final = "endpoints/{environment_id}"


API_RECREATE: Final = "docker/{environment_id}/containers/{container_id}/recreate"
API_IMAGE_STATUS: Final = (
    "docker/{environment_id}/containers/{container_id}/image_status"
)
API_STATS: Final = "endpoints/{environment_id}/docker/containers/{container_id}/stats"
API_CONTAINER_STOP: Final = (
    "endpoints/{environment_id}/docker/containers/{container_id}/stop"
)
API_CONTAINER_START: Final = (
    "endpoints/{environment_id}/docker/containers/{container_id}/start"
)
API_CONTAINER_RESTART: Final = (
    "endpoints/{environment_id}/docker/containers/{container_id}/restart"
)
