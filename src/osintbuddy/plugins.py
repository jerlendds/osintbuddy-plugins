from __future__ import annotations
import hashlib
from typing import List
from osintbuddy.utils import slugify
from fastapi import APIRouter

# @todo


class BasePlugin(object):
    def __init__(self) -> None:
        self.transforms: dict = None
        self.node: dict = None
        self.node_name: str = None
        self.settings: dict = None
        self.repository: str = None
        self.authors = List[str]
        self._base_plugin_endpoint = slugify(self.node_name)
        self._router: APIRouter = APIRouter(prefix=self._base_plugin_endpoint)
        self._generate_endpoints()

    def request(self, transform: str, **kwargs):
        return self.transforms[transform](**kwargs)

    def _generate_endpoints(self):
        if self.transforms is None:
            return
        for transform in self.transforms.keys():
            route = str.encode(
                f"{self._base_plugin_endpoint}{transform}{self.repository}"
            )
            endpoint_route = hashlib.md5(route).hexdigest()
            self._router.add_api_route(
                endpoint_route,
                endpoint=self.transforms[transform]
            )


class Plugin(BasePlugin):
    def __init__(self):
        pass
