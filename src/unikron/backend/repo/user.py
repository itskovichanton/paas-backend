from src.mybootstrap_core_itskovichanton.orm import infer_where, to_real_entity
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_pyauth_itskovichanton.backend.user_repo import UserRepo
from src.mybootstrap_pyauth_itskovichanton.entities import User

from src.unikron.backend.repo.db import DB
from src.unikron.backend.repo.schema import UserM, DictUserStatusM, ServiceM, CountryM, CategoryM, DictUserPermissionM, \
    UserPermissionM


@bean
class DBUserRepoImpl(UserRepo):

    def init(self, **kwargs):
        self._service_users: dict[id, User] = {}

    def put(self, a: User):
        if a.id and a.id < 0:
            self._service_users[a.id] = a

    @to_real_entity
    def find(self, criteria: User) -> User:
        if criteria.id and criteria.id < 0:
            return self._service_users.get(criteria.id)

        r = (UserM.select(UserM, DictUserStatusM)
             .limit(1)
             .join(DictUserStatusM, on=(DictUserStatusM.id == UserM.status))
             .where(UserM.username == criteria.username))
        if r:
            r = r[0]
            r.permissions = [x.name for x in self._get_user_permissions(r.id)]
            r.status = r.status.name

        return r

    @staticmethod
    def _get_user_permissions(user_id):
        return [x.dictuserpermissionm for x in
                (UserPermissionM.select(UserPermissionM, DictUserPermissionM)
                 .join(DictUserPermissionM, on=(DictUserPermissionM.id == UserPermissionM.permission_id))
                 .where(UserPermissionM.user_id == user_id))]
