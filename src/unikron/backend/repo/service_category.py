from typing import Protocol

from src.mybootstrap_core_itskovichanton.orm import infer_where, to_real_entity
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_pyauth_itskovichanton.backend.user_repo import UserRepo
from src.mybootstrap_pyauth_itskovichanton.entities import User

from src.unikron.backend.entity.common import ServiceCategory
from src.unikron.backend.repo.db import DB
from src.unikron.backend.repo.schema import UserM, DictUserStatusM, ServiceM, CountryM, ServiceCategoryM, \
    DictUserPermissionM, \
    UserPermissionM


class ServiceCategoryRepo(Protocol):

    def all(self) -> list[ServiceCategory]:
        ...


@bean
class ServiceCategoryRepoImpl(ServiceCategoryRepo):

    @to_real_entity
    def all(self) -> list[ServiceCategory]:
        return ServiceCategoryM.select(ServiceCategoryM)
