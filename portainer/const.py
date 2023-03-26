"""Library constants."""
from typing import Final

# APIs
API_AUTH: Final = "auth"                                            # POST
API_ENDPOINTS: Final = "endpoints"                                  # GET
API_ENDPOINT: Final = "endpoints/{}"                                # GET


API_RECREATE: Final = "docker/{}/containers/{}/recreate"            # POST
API_IMAGE_STATUS: Final = "docker/{}/containers/{}/image_status"    # GET
API_STATS: Final = "endpoints/{}/docker/containers/{}/stats"        # GET
