from dataclasses import dataclass
from typing import Protocol

import requests
from dacite import from_dict, Config
from src.mybootstrap_core_itskovichanton.realtime_config import RealTimeConfigEntry
from src.mybootstrap_core_itskovichanton.utils import is_listable
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_mvc_fastapi_itskovichanton.utils import parse_response
from src.mybootstrap_pyauth_itskovichanton.entities import AuthArgs

from src.unikron.backend.entity.common import Deploy


@dataclass
class _Config:
    s2s: AuthArgs = None


@dataclass
class ETCDListing:
    key_prefix: str = None
    data: dict[str, RealTimeConfigEntry] = None


class Replicas(Protocol):

    def list_etcds(self, replica_url) -> ETCDListing:
        ...


@bean(config=("replicas", _Config, _Config()))
class ReplicasImpl(Replicas):

    def init(self, **kwargs):
        self._session = requests.Session()
        if self.config.s2s:
            self._session.auth = (self.config.s2s.username, self.config.s2s.password)
        self._session.timeout = 5

    def list_etcds(self, replica_url) -> ETCDListing:
        r = parse_response(self._session.get(url=f"{replica_url}/etcd/list"), cl=ETCDListing)
        r.data = {p.get("key"): p for p in r.data}
        return r
