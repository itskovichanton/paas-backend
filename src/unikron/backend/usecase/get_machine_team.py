from typing import Protocol

from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_pyauth_itskovichanton.entities import Session
from src.mybootstrap_pyauth_itskovichanton.frontend.controller import GetUserAction, GetUserActionParams

from src.unikron.backend.entity.common import SearchServiceQuery, Service, USER_PERMISSION_CONTROL_SERVICE, \
    USER_PERMISSION_READ_SERVICE, USER_PERMISSION_READ_DEPLOYS
from src.unikron.backend.repo.machine import MachineRepo
from src.unikron.backend.repo.service import ServiceRepo
from src.unikron.backend.usecase.check_account_permission import CheckAccountPermissionUseCase


class GetMachineTeamUseCase(Protocol):

    def get(self, session: Session, ip):
        ...


@bean
class GetMachineTeamUseCaseImpl(GetMachineTeamUseCase):
    check_permissions_uc: CheckAccountPermissionUseCase
    get_user_action: GetUserAction
    service_repo: MachineRepo

    def get(self, session: Session, ip):
        session = self.get_user_action.run(session)
        self.check_permissions_uc.check_permission(session, USER_PERMISSION_READ_DEPLOYS)
        return self.service_repo.get_team(ip) or []
