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


class ServiceRepo(Protocol):

    def get_team(self, service: str):
        ...

    def search_services(self, q: SearchServiceQuery = None) -> list[Service]:
        ...


def _select_services(q: SearchServiceQuery):
    return ServiceM.select(*ServiceM.get_short_fields(), ServiceCategoryM, CountryM) if q.short \
        else ServiceM.select(ServiceM, ServiceCategoryM, CountryM)


@bean
class ServiceRepoImpl(ServiceRepo):
    db: DB

    def search_services(self, q: SearchServiceQuery = None) -> list[Service]:
        r = self._search_services(q)
        if not r:
            return r

        service_dict = {x.id: x for x in r}
        for x in self._get_teams(list(service_dict.keys())):
            service = service_dict[x.service_id]
            if service.team is None:
                service.team = {}
            service.team[x.user_id] = ServiceTeammate(account=x.userm, service_role=x.user_role)

        for service in r:

            if service.team:
                service.team = list(service.team.values())
                service.team.sort(key=lambda t: t.account.id)
            else:
                service.team = []

        return r

    @to_real_entity
    def _get_teams(self, service_ids):
        return (UserServiceRolesM.select(UserServiceRolesM, *UserM.get_public_fields())
                .join(UserM, on=(UserM.id == UserServiceRolesM.user_id))
                .where(UserServiceRolesM.service_id << service_ids))

    @to_real_entity
    def _search_services(self, q: SearchServiceQuery = None):
        r = _select_services(q)
        r = (r.join(ServiceCategoryM, on=(ServiceCategoryM.id == ServiceM.category))
             .join(CountryM, on=(CountryM.id == ServiceM.country)))

        if not q:
            return r
        if q.limit:
            r = r.limit(q.limit)
        if q.id:
            r = r.where(ServiceM.id == q.id)
        else:
            if q.country_id:
                r = r.where(CountryM.id == q.country_id)
            if q.category_id:
                r = r.where(ServiceCategoryM.id == q.category_id)
            if q.query:
                query_upper = q.query.upper()
                r = r.where(fn.Upper(ServiceM.name).contains(query_upper) |
                            fn.Upper(ServiceM.title).contains(query_upper) |
                            fn.Upper(ServiceM.description).contains(query_upper) |
                            fn.Upper(CountryM.name).contains(query_upper) |
                            fn.Upper(ServiceM.tags).contains(query_upper) |
                            fn.Upper(ServiceCategoryM.name).contains(query_upper))

        return r

    def get_team(self, service: str):

        q = """select u.id, u.username, u.email, u.name, u.telegram_username, usr.user_role from public.user u
        inner join public.user_service_roles usr on usr.user_id=u.id
        inner join public.service s on s.id=usr.service_id
        where s.name = %s"""

        return self.db.exec_sql(query=q, params=[service])
