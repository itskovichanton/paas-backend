from typing import Protocol

from peewee import fn
from src.mybootstrap_core_itskovichanton.orm import infer_where, to_real_entity
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_pyauth_itskovichanton.backend.user_repo import UserRepo
from src.mybootstrap_pyauth_itskovichanton.entities import User

from src.unikron.backend.entity.common import SearchServiceQuery, ServiceTeammate, Service
from src.unikron.backend.repo.db import DB
from src.unikron.backend.repo.schema import UserM, DictUserStatusM, ServiceM, CountryM, ServiceCategoryM, \
    DictUserPermissionM, \
    UserPermissionM, UserServiceRolesM


class MachineRepo(Protocol):

    def get_team(self, ip: str):
        ...


@bean
class MachineRepoImpl(MachineRepo):
    db: DB

    def get_team(self, ip: str):
        q = """select u.id, u.username, u.email, u.name, u.telegram_username, usr.user_role from public.user u
        inner join public.user_service_roles usr on usr.user_id=u.id
        inner join public.service s on s.id=usr.service_id
        where s.name = %s"""

        return self.db.exec_sql(query=q, params=[ip])
