from typing import Protocol

from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_pyauth_itskovichanton.entities import Session
from src.mybootstrap_pyauth_itskovichanton.frontend.controller import GetUserAction, GetUserActionParams

from src.unikron.backend.entity.common import SearchServiceQuery, Service, USER_PERMISSION_CONTROL_SERVICE, \
    USER_PERMISSION_READ_SERVICE, Commons
from src.unikron.backend.repo.country import CountryRepo
from src.unikron.backend.repo.service import ServiceRepo
from src.unikron.backend.repo.service_category import ServiceCategoryRepo
from src.unikron.backend.usecase.check_account_permission import CheckAccountPermissionUseCase


class GetCommonsUseCase(Protocol):

    def get(self, session: Session) -> Commons:
        ...


@bean
class GetCommonsUseCaseImpl(GetCommonsUseCase):
    get_user_action: GetUserAction
    service_category_repo: ServiceCategoryRepo
    country_repo: CountryRepo

    def get(self, session: Session) -> Commons:
        session = self.get_user_action.run(session)
        return Commons(service_categories=self.service_category_repo.all(), countries=self.country_repo.all())
