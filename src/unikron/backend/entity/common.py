import datetime
from dataclasses import dataclass

from src.mbulak_tools.entities import Account
from src.mybootstrap_core_itskovichanton.utils import hashed

USER_PERMISSION_CONTROL_SERVICE = "control_service"
USER_PERMISSION_WRITE_ETCD = "write_etcd"
USER_PERMISSION_READ_SERVICE = "read_service"


@hashed
@dataclass
class SearchServiceQuery:
    query: str = None
    category_id: int = None
    country_id: int = None


@hashed
@dataclass
class ServiceCategory:
    id: int = None
    name: str = None


@hashed
@dataclass
class UserPermission:
    id: int = None
    name: str = None


@hashed
@dataclass
class UserStatus:
    id: int = None
    name: str = None


@hashed
@dataclass
class Country:
    id: int = None
    name: str = None
    strid: str = None


@hashed
@dataclass
class ServiceTeammate:
    account: Account = None
    service_role: str = None


@hashed
@dataclass
class Service:
    id: int = None
    name: str = None
    title: str = None
    category: ServiceCategory = None
    country: Country = None
    created_at: datetime = None
    description: str = None
    gitlab_url: str = None
    gitlab_project_id: int = None
    longread: str = None
    tags: str = None
    cherkizon_service: str = None
    team: list[ServiceTeammate] = None


@hashed
@dataclass
class Commons:
    service_categories: list[ServiceCategory] = None
    countries: list[Country] = None
