from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_mvc_itskovichanton.pipeline import ActionRunner
from src.mybootstrap_pyauth_itskovichanton.entities import Caller

from src.unikron.backend.entity.common import SearchServiceQuery
from src.unikron.backend.usecase.get_commons import GetCommonsUseCase
from src.unikron.backend.usecase.search_services import SearchServicesUseCase


@bean
class Controller:
    action_runner: ActionRunner
    search_services_uc: SearchServicesUseCase
    get_commons_uc: GetCommonsUseCase

    async def get_commons(self, caller: Caller):
        return await self.action_runner.run(self.get_commons_uc.get,
                                            call={"session": caller.session}, unbox_call=True)

    async def search_services(self, caller: Caller, query: SearchServiceQuery):
        return await self.action_runner.run(self.search_services_uc.search,
                                            call={"session": caller.session, "q": query}, unbox_call=True)
