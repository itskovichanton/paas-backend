from typing import Protocol

from src.mybootstrap_core_itskovichanton.orm import infer_where, to_real_entity
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_pyauth_itskovichanton.backend.user_repo import UserRepo
from src.mybootstrap_pyauth_itskovichanton.entities import User

from src.unikron.backend.repo.db import DB
from src.unikron.backend.repo.schema import UserM, DictUserStatusM, ServiceM, CountryM, ServiceCategoryM, \
    DictUserPermissionM, \
    UserPermissionM


class UserPermissionRepo(Protocol):

    def has_permission(self, account_id, *args) -> bool:
        ...

    def get_permissions(self, user_id):
        ...


@bean
class UserPermissionRepoImpl(UserPermissionRepo):

    def has_permission(self, account_id, *args) -> bool:
        return (UserPermissionM.select(UserPermissionM, DictUserPermissionM)
                .join(DictUserPermissionM, on=(DictUserPermissionM.id == UserPermissionM.permission_id))
                .where(UserPermissionM.user_id == account_id and DictUserPermissionM.name << args).count()) == len(args)
    #
    # @to_real_entity
    # def get_permissions(self, account_id):
    #     return [x.dictuserpermissionm for x in
    #             (UserPermissionM.select(UserPermissionM, DictUserPermissionM)
    #              .join(DictUserPermissionM, on=(DictUserPermissionM.id == UserPermissionM.permission_id))
    #              .where(UserPermissionM.user_id == account_id))]
