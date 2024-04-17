import uvicorn
from fastapi import FastAPI
from src.mbulak_tools.apis.hc.frontend.support import HealthcheckFastAPISupport
from src.mybootstrap_core_itskovichanton.logger import LoggerService
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_ioc_itskovichanton.utils import default_dataclass_field
from src.mybootstrap_mvc_fastapi_itskovichanton.error_handler import ErrorHandlerFastAPISupport
from src.mybootstrap_mvc_fastapi_itskovichanton.middleware_logging import HTTPLoggingMiddleware
from src.mybootstrap_mvc_fastapi_itskovichanton.presenters import JSONResultPresenterImpl
from src.mybootstrap_mvc_itskovichanton.result_presenter import ResultPresenter
from src.mybootstrap_pyauth_itskovichanton.frontend.support import AuthFastAPISupport
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.unikron.frontend.controller import Controller


@bean(port=("server.port", int, 8082), host=("server.host", str, "0.0.0.0"))
class Server:
    error_handler_fast_api_support: ErrorHandlerFastAPISupport
    healthcheck_support: HealthcheckFastAPISupport
    auth_support: AuthFastAPISupport
    presenter: ResultPresenter = default_dataclass_field(JSONResultPresenterImpl(exclude_unset=True))
    controller: Controller
    logger_service: LoggerService

    def init(self, **kwargs):
        self.fast_api = self.init_fast_api()
        self.add_routes()

    def start(self):
        uvicorn.run(self.fast_api, port=self.port, host=self.host)

    def init_fast_api(self) -> FastAPI:
        r = FastAPI(title='unikron', debug=False)
        self.error_handler_fast_api_support.mount(r)
        self.healthcheck_support.mount(r)
        self.auth_support.mount(r)
        r.add_middleware(HTTPLoggingMiddleware, encoding="utf-8", logger=self.logger_service.get_file_logger("http"))
        r.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        return r

    def add_routes(self):
        ...

        # @self.fast_api.post("/service/find")
        # async def service_find(request: Request, q: SearchServiceQuery):
        #     return self.presenter.present(await self.controller.find_services(q))
