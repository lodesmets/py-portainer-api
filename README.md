# py-portainer-api

Python library to interface with portainer

# WARNING this is still very alpha, and a lot will change

# Usage

You can import the module as `portainer`.

## Constructor

```python
Portainer(
    portainer_ip: str,
    portainer_port: int,
    username: str,
    password: str,
    use_https: bool = False,
    debugmode: bool = False,
)
```

## Code example

```python
import asyncio

from portainer import Portainer
from portainer.exceptions import PortainerException

portainer = Portainer("192.168.0.100", 9000, "admin", "Password")
try:
    asyncio.run(portainer.login())
except PortainerException:
    print("Error")

endpoints = asyncio.run(portainer.get_endpoints())
if endpoints is None:
    print("No endpoints found")
else:
    asyncio.run(endpoints[0].refresh())
    asyncio.run(endpoints[0].docker_container["grocy"].get_image_status())
    asyncio.run(endpoints[0].docker_container["grocy"].get_stats())
    asyncio.run(endpoints[0].docker_container["grocy"].recreate())
```
