"""Portainer tests."""

import asyncio

from portainer import Portainer
from portainer.exceptions import PortainerException

portainer = Portainer("192.168.0.100", 9000, "admin", "7CdWy9VzsVHbB4M!")
try:
    asyncio.run(portainer.login())
except PortainerException:
    print("Error")

endpoints = asyncio.run(portainer.get_endpoints())

asyncio.run(endpoints[0].refresh())
asyncio.run(endpoints[0]._docker_container["lode_grocy"].get_image_status())
asyncio.run(endpoints[0]._docker_container["lode_grocy"].get_stats())
asyncio.run(endpoints[0]._docker_container["lode_grocy"].recreate())
