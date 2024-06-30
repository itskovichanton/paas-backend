from dataclasses import dataclass
from typing import Protocol

import requests
from dacite import from_dict, Config
from src.mybootstrap_core_itskovichanton.utils import is_listable, to_dict_deep
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_mvc_fastapi_itskovichanton.utils import parse_response
from src.mybootstrap_pyauth_itskovichanton.entities import AuthArgs

from src.unikron.backend.entity.common import Deploy, DeployQuery, DeployListing


@dataclass
class _Config:
    url: str = None
    s2s: AuthArgs = None


class Cherkizon(Protocol):

    def search_deploys(self, filter: Deploy) -> DeployListing:
        ...


@bean(config=("cherkzion", _Config, _Config()))
class CherkizonImpl(Cherkizon):

    def init(self, **kwargs):
        self._session = requests.Session()
        if self.config.s2s:
            self._session.auth = (self.config.s2s.username, self.config.s2s.password)
        self._session.timeout = 5

    def search_deploys(self, filter: Deploy) -> DeployListing:
        return parse_response(self._session.post(url=self._get_endpoint_url("deploy/list"), json=to_dict_deep(filter)),
                              cl=DeployListing)

    def _get_endpoint_url(self, endpoint):
        return f"{self.config.url}/{endpoint}"
