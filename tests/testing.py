"""Portainer tests."""

import asyncio

import aiohttp

from portainer import Portainer
from portainer.exceptions import PortainerException


async def main():
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        await do(session)


async def do(session: aiohttp.ClientSession):
    portainer = Portainer(session, "192.168.0.100", 9000, "admin", "Password")
    try:
        await portainer.login()
    except PortainerException:
        print("Error")
        return

    endpoints = await portainer.get_endpoints()
    if endpoints is None:
        print("No endpoints found")
    else:
        await endpoints[0].refresh()
        await endpoints[0].docker_container["lode_grocy"].get_image_status()
        await endpoints[0].docker_container["lode_grocy"].get_stats()
        await endpoints[0].docker_container["lode_grocy"].recreate()


if __name__ == "__main__":
    asyncio.run(main())
