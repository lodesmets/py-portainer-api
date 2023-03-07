"""Portainer tests."""

from portainer import Portainer
import asyncio

portainer = Portainer("192.168.0.100", 9000, "admin", "7CdWy9VzsVHbB4M!")
try:
    asyncio.run(portainer.login())
except:
    print("Error")

asyncio.run(portainer.getEndpoints())
#try:
#except:
#    print("Error")
