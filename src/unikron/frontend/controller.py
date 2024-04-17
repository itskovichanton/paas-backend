from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_mvc_itskovichanton.pipeline import ActionRunner




@bean
class Controller:
    action_runner: ActionRunner

    # find_services_uc: FindServicesUseCase

    # async def find_services(self, q: SearchServiceQuery):
    #     return await self.action_runner.run(self.find_services_uc.find, call=q)
