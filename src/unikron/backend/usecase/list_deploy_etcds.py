from typing import Protocol

from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_mvc_itskovichanton.exceptions import CoreException, \
    ERR_REASON_SERVER_RESPONDED_WITH_ERROR_NOT_FOUND
from src.mybootstrap_pyauth_itskovichanton.entities import Session
from src.mybootstrap_pyauth_itskovichanton.frontend.controller import GetUserAction, GetUserActionParams

from src.unikron.backend.apis.cherkizon import Cherkizon
from src.unikron.backend.apis.replicas import Replicas
from src.unikron.backend.entity.common import SearchServiceQuery, Service, USER_PERMISSION_CONTROL_SERVICE, \
    USER_PERMISSION_READ_SERVICE, USER_PERMISSION_READ_DEPLOYS, Deploy, USER_PERMISSION_READ_ETCDS, DeployQuery
from src.unikron.backend.repo.service import ServiceRepo
from src.unikron.backend.usecase.check_account_permission import CheckAccountPermissionUseCase
from src.unikron.backend.usecase.search_deploys import SearchDeploysUseCase


class ListDeploysETCDsUseCase(Protocol):

    def search(self, session: Session, filter: DeployQuery) -> list[Deploy]:
        ...


@bean
class ListDeploysETCDsUseCaseImpl(ListDeploysETCDsUseCase):
    check_permissions_uc: CheckAccountPermissionUseCase
    search_deploys_uc: SearchDeploysUseCase
    get_user_action: GetUserAction
    replicas: Replicas

    def search(self, session: Session, filter: DeployQuery) -> list[Deploy]:
        session = self.get_user_action.run(session)
        self.check_permissions_uc.check_permission(session, USER_PERMISSION_READ_ETCDS)
        deploys = self.search_deploys_uc.search(session, filter).deploys

        if not deploys:
            raise CoreException(message="деплоев не найдено",
                                reason=ERR_REASON_SERVER_RESPONDED_WITH_ERROR_NOT_FOUND)
        if len(deploys) != 1:
            raise CoreException(message="должен быть ровно 1 деплой")

        deploy = deploys[0]

        deploy.internal_url="http://localhost:3333"
        etcds = self.replicas.list_etcds(deploy.internal_url)
        return etcds
