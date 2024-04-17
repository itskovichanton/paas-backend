import datetime
from dataclasses import dataclass

from src.mybootstrap_core_itskovichanton.utils import hashed


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


@hashed
@dataclass
class Service:
    id: int = None
    name: str = None
    title: str = None
    category_id: ServiceCategory = None
    country_id = Country = None
    created_at: datetime = None
    description: str = None
    gitlab_id: int = None
    gitlab_url: str = None
    longread: str = None
    name: str = None
    tags: str = None
    cherkizon_service: str = None
