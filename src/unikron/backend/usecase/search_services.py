from typing import Protocol

from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_pyauth_itskovichanton.entities import Session
from src.mybootstrap_pyauth_itskovichanton.frontend.controller import GetUserAction, GetUserActionParams

from src.unikron.backend.entity.common import SearchServiceQuery, Service, USER_PERMISSION_CONTROL_SERVICE, \
    USER_PERMISSION_READ_SERVICE
from src.unikron.backend.repo.service import ServiceRepo
from src.unikron.backend.usecase.check_account_permission import CheckAccountPermissionUseCase


class SearchServicesUseCase(Protocol):

    def search(self, session: Session, q: SearchServiceQuery = None) -> list[Service]:
        ...


@bean
class SearchServicesUseCaseImpl(SearchServicesUseCase):
    check_permissions_uc: CheckAccountPermissionUseCase
    get_user_action: GetUserAction
    service_repo: ServiceRepo

    def search(self, session: Session, q: SearchServiceQuery = None) -> list[Service]:
        session = self.get_user_action.run(session)
        self.check_permissions_uc.check_permission(session, USER_PERMISSION_READ_SERVICE)
        services = self.service_repo.find_services(q) or []
        for service in services:
            if service.tags:
                service.tags = [s.strip() for s in service.tags.split(",")]
        return services
