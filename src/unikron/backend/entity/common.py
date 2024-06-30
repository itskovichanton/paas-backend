import datetime
from dataclasses import dataclass

from src.mybootstrap_core_itskovichanton.utils import hashed
from src.mybootstrap_pyauth_itskovichanton.entities import User

USER_PERMISSION_CONTROL_SERVICE = "control_service"
USER_PERMISSION_WRITE_ETCD = "write_etcd"
USER_PERMISSION_READ_SERVICE = "read_service"
USER_PERMISSION_READ_DEPLOYS = "read_deploys"
USER_PERMISSION_READ_ETCDS = "read_etcds"
USER_PERMISSION_WRITE_ETCDS = "write_etcds"


@dataclass
class SearchServiceQuery:
    query: str = None
    category_id: int = None
    country_id: int = None
    id: int = None
    limit: int = None
    short: bool = False


@dataclass
class ServiceCategory:
    id: int = None
    name: str = None


@dataclass
class UserPermission:
    id: int = None
    name: str = None


@dataclass
class UserStatus:
    id: int = None
    name: str = None


@dataclass
class Country:
    id: int = None
    name: str = None
    strid: str = None


@dataclass
class ServiceTeammate:
    account: User = None
    service_role: str = None


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


@dataclass
class Commons:
    service_categories: list[ServiceCategory] = None
    countries: list[Country] = None


@dataclass
class User:
    username: str
    id: int
    name: str
    email: str = None
    telegram_username: str = None
    user_role: str = None


@dataclass
class CPU:
    load: float


@dataclass
class MemoryVolume:
    available: int
    used: int
    total: int


@dataclass
class MachineInfo:
    ip: str = None
    available: bool = False  # машина доступна
    connection_error: str = None
    ram: MemoryVolume = None  # из free -h
    disk: MemoryVolume = None  # из df -h
    cpu: CPU = None
    etcd_port: int = None


@dataclass
class HealthcheckResult:
    result: dict = None
    service_name: str = None
    time: datetime.datetime = None

    def is_failed(self) -> bool:
        return "error" in self.result


@dataclass
class Machine:
    ip: str = None
    name: str = None
    env: str = None
    description: str = None
    info: MachineInfo = None
    etcd_port: int = None


@dataclass
class Deploy:
    port: str = None
    metrics_url: str = None
    last_start: datetime.datetime = None
    connection_error: str = None
    port_status: str = None
    pid: str = None
    status: str = None
    active: str = None
    load: str = None
    name: str = None
    systemd_name: str = None
    url: str = None
    internal_url: str = None
    machine: Machine = None
    version: str = None
    author: str = None
    env: str = None
    healthcheck_result: HealthcheckResult = None


@dataclass
class DeployQuery:
    name: str = None
    systemd_name: str = None
    env: str = None


@dataclass
class DeployListing:
    deploys: list[Deploy] = None
    machines: dict[str, Machine] = None
