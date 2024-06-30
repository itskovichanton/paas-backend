from typing import Protocol

from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_pyauth_itskovichanton.entities import Session
from src.mybootstrap_pyauth_itskovichanton.frontend.controller import GetUserAction, GetUserActionParams

from src.unikron.backend.apis.cherkizon import Cherkizon
from src.unikron.backend.entity.common import SearchServiceQuery, Service, USER_PERMISSION_CONTROL_SERVICE, \
    USER_PERMISSION_READ_SERVICE, USER_PERMISSION_READ_DEPLOYS, Deploy, DeployQuery, DeployListing
from src.unikron.backend.repo.service import ServiceRepo
from src.unikron.backend.usecase.check_account_permission import CheckAccountPermissionUseCase


class SearchDeploysUseCase(Protocol):

    def search(self, session: Session, filter: DeployQuery) -> DeployListing:
        ...


@bean
class SearchDeploysUseCaseImpl(SearchDeploysUseCase):
    check_permissions_uc: CheckAccountPermissionUseCase
    get_user_action: GetUserAction
    cherkizon: Cherkizon

    def search(self, session: Session, filter: DeployQuery) -> DeployListing:
        session = self.get_user_action.run(session)
        self.check_permissions_uc.check_permission(session, USER_PERMISSION_READ_DEPLOYS)
        deploys = self.cherkizon.search_deploys(filter)
        return deploys
