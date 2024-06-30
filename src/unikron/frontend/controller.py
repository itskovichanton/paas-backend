from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_mvc_itskovichanton.pipeline import ActionRunner
from src.mybootstrap_pyauth_itskovichanton.entities import Caller

from src.unikron.backend.entity.common import SearchServiceQuery, Deploy, DeployQuery
from src.unikron.backend.usecase.get_commons import GetCommonsUseCase

from src.unikron.backend.usecase.get_service_team import GetServiceTeamUseCase
from src.unikron.backend.usecase.list_deploy_etcds import ListDeploysETCDsUseCase
from src.unikron.backend.usecase.search_deploys import SearchDeploysUseCase
from src.unikron.backend.usecase.search_services import SearchServicesUseCase


@bean
class Controller:
    action_runner: ActionRunner
    search_services_uc: SearchServicesUseCase
    get_commons_uc: GetCommonsUseCase
    get_service_team_uc: GetServiceTeamUseCase
    search_deploys_uc: SearchDeploysUseCase
    list_deploys_ETCDs_uc: ListDeploysETCDsUseCase

    async def get_commons(self, caller: Caller):
        return await self.action_runner.run(self.get_commons_uc.get,
                                            call={"session": caller.session}, unbox_call=True)

    async def search_services(self, caller: Caller, query: SearchServiceQuery):
        return await self.action_runner.run(self.search_services_uc.search,
                                            call={"session": caller.session, "q": query}, unbox_call=True)

    async def get_service_team(self, caller: Caller, service):
        return await self.action_runner.run(self.get_service_team_uc.get,
                                            call={"session": caller.session, "service": service}, unbox_call=True)

    async def search_deploys(self, caller: Caller, filter: DeployQuery):
        return await self.action_runner.run(self.search_deploys_uc.search,
                                            call={"session": caller.session, "filter": filter}, unbox_call=True)

    async def get_deploy_etcd_list(self, caller: Caller, filter: DeployQuery):
        return await self.action_runner.run(self.list_deploys_ETCDs_uc.search,
                                            call={"session": caller.session, "filter": filter}, unbox_call=True)
