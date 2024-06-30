from typing import Protocol

from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_mvc_itskovichanton.exceptions import CoreException, \
    ERR_REASON_SERVER_RESPONDED_WITH_ERROR_NOT_FOUND
from src.mybootstrap_pyauth_itskovichanton.entities import Session
from src.mybootstrap_pyauth_itskovichanton.frontend.controller import GetUserAction, GetUserActionParams

from src.unikron.backend.apis.cherkizon import Cherkizon
from src.unikron.backend.entity.common import SearchServiceQuery, Service, USER_PERMISSION_CONTROL_SERVICE, \
    USER_PERMISSION_READ_SERVICE, USER_PERMISSION_READ_DEPLOYS, Deploy, DeployQuery, DeployListing
from src.unikron.backend.repo.service import ServiceRepo
from src.unikron.backend.usecase.check_account_permission import CheckAccountPermissionUseCase


class SearchDeploysUseCase(Protocol):

    def search(self, session: Session, filter: Deploy) -> DeployListing:
        ...

    def search_one(self, session: Session, filter: Deploy) -> DeployListing:
        ...


@bean
class SearchDeploysUseCaseImpl(SearchDeploysUseCase):
    check_permissions_uc: CheckAccountPermissionUseCase
    get_user_action: GetUserAction
    cherkizon: Cherkizon

    def search(self, session: Session, filter: Deploy) -> DeployListing:
        session = self.get_user_action.run(session)
        self.check_permissions_uc.check_permission(session, USER_PERMISSION_READ_DEPLOYS)
        deploys = self.cherkizon.search_deploys(filter)
        return deploys

    def search_one(self, session: Session, filter: Deploy) -> DeployListing:
        deploys_listing = self.search(session, filter)

        if not deploys_listing:
            raise CoreException(message="деплоев не найдено",
                                reason=ERR_REASON_SERVER_RESPONDED_WITH_ERROR_NOT_FOUND)
        if len(deploys_listing.deploys) != 1:
            raise CoreException(message="должен быть ровно 1 деплой")

        return deploys_listing
