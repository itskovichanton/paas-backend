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

    def find_services(self, q: SearchServiceQuery = None) -> list[Service]:
        ...


@bean
class ServiceRepoImpl(ServiceRepo):

    def find_services(self, q: SearchServiceQuery = None) -> list[Service]:
        r = self._find_services(q, short=True)
        if not r:
            return r

        service_dict = {x.id: x for x in r}
        for x in self._get_teams(list(service_dict.keys())):
            service = service_dict[x.service_id]
            if service.team is None:
                service.team = {}
            service.team[x.user_id] = ServiceTeammate(account=x.userm, service_role=x.user_role)

        for service in r:
            service.team = list(service.team.values())
            service.team.sort(key=lambda t: t.account.id)

        return r

    @to_real_entity
    def _get_teams(self, service_ids):
        return (UserServiceRolesM.select(UserServiceRolesM, *UserM.get_public_fields())
                .join(UserM, on=(UserM.id == UserServiceRolesM.user_id))
                .where(UserServiceRolesM.service_id << service_ids))

    @to_real_entity
    def _find_services(self, q: SearchServiceQuery = None, short=True):
        r = (ServiceM.select(*ServiceM.get_short_fields() if short else ServiceM, ServiceCategoryM, CountryM)
             .join(ServiceCategoryM, on=(ServiceCategoryM.id == ServiceM.category))
             .join(CountryM, on=(CountryM.id == ServiceM.country)))

        if not q:
            return r

        if q.country_id:
            r = r.where(CountryM.id == q.country_id)
        if q.category_id:
            r = r.where(ServiceCategoryM.id == q.category_id)
        if q.query:
            query_upper = q.query.upper()
            r = r.where(fn.Upper(ServiceM.name).contains(query_upper) |
                        fn.Upper(ServiceM.title).contains(query_upper) |
                        fn.Upper(ServiceM.description).contains(query_upper) |
                        fn.Upper(ServiceCategoryM.name).contains(query_upper) |
                        fn.Upper(CountryM.name).contains(query_upper))

        return r
