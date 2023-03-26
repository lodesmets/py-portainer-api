"""Portainer tests."""

from portainer import Portainer
import asyncio

portainer = Portainer("192.168.0.100", 9000, "admin", "7CdWy9VzsVHbB4M!")
try:
    asyncio.run(portainer.login())
except:
    print("Error")

endpoints = asyncio.run(portainer.getEndpoints())

asyncio.run(endpoints[0].refresh())
asyncio.run(endpoints[0]._dockerContainer['lode_grocy'].getImageStatus())
asyncio.run(endpoints[0]._dockerContainer['lode_grocy'].getStats())
asyncio.run(endpoints[0]._dockerContainer['lode_grocy'].recreate())