import os.path

import uvicorn
from fastapi import FastAPI
from src.mybootstrap_core_itskovichanton.logger import LoggerService
from src.mybootstrap_ioc_itskovichanton.config import ConfigService
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_ioc_itskovichanton.utils import default_dataclass_field
from src.mybootstrap_mvc_fastapi_itskovichanton.error_handler import ErrorHandlerFastAPISupport
from src.mybootstrap_mvc_fastapi_itskovichanton.middleware_logging import HTTPLoggingMiddleware
from src.mybootstrap_mvc_fastapi_itskovichanton.presenters import JSONResultPresenterImpl
from src.mybootstrap_mvc_itskovichanton.result_presenter import ResultPresenter
from src.mybootstrap_pyauth_itskovichanton.frontend.support import AuthFastAPISupport
from src.mybootstrap_pyauth_itskovichanton.frontend.utils import get_caller_from_request
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse

from src.unikron.backend.entity.common import SearchServiceQuery, Deploy, DeployQuery
from src.unikron.frontend.controller import Controller


@bean(port=("server.port", int, 8082), host=("server.host", str, "0.0.0.0"))
class Server:
    config_service: ConfigService
    error_handler_fast_api_support: ErrorHandlerFastAPISupport
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
        @self.fast_api.get("/service/team")
        async def get_service_team(request: Request, service):
            return self.presenter.present(
                await self.controller.get_service_team(caller=get_caller_from_request(request), service=service),
            )

        @self.fast_api.post("/service/search")
        async def service_search(request: Request, q: SearchServiceQuery):
            return self.presenter.present(
                await self.controller.search_services(caller=get_caller_from_request(request), query=q),
            )

        @self.fast_api.get("/commons")
        async def service_search(request: Request):
            return self.presenter.present(
                await self.controller.get_commons(caller=get_caller_from_request(request)),
            )

        @self.fast_api.get("/static")
        async def get_image(filename: str):
            return FileResponse(os.path.join(self.config_service.dir("static"), filename))

        @self.fast_api.post("/deploy/search")
        async def search_deploys(request: Request, filter: DeployQuery):
            return self.presenter.present(
                await self.controller.search_deploys(caller=get_caller_from_request(request), filter=filter))

        @self.fast_api.post("/deploy/etcd/list")
        async def get_deploy_etcd_list(request: Request, filter: DeployQuery):
            return self.presenter.present(
                await self.controller.get_deploy_etcd_list(caller=get_caller_from_request(request), filter=filter))
