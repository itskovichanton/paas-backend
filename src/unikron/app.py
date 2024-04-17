from src.mybootstrap_core_itskovichanton.app import Application
from src.mybootstrap_core_itskovichanton.logger import LoggerService
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_pyauth_itskovichanton.backend.auth import Authentificator

from src.unikron.backend.repo.db import DB
from src.unikron.backend.repo.user import DBUserRepoImpl

from src.unikron.frontend.server import Server


@bean
class UnikronApp(Application):
    server: Server
    db: DB
    user_repo: DBUserRepoImpl
    auther: Authentificator
    # uc1: GetDeployUrlUseCase
    # file_content_provider: BatchFileWriter
    # batch_file_validator: BatchFileValidator
    # batch_file_content_filter: BatchFileContentFilter
    # packer: BatchFilePacker
    # fm: FileManagerClient
    # order_repo: OrderRepo

    logger_service: LoggerService

    def run(self):
        self.auther.user_repo = self.user_repo
        # self.events.subscribe_on_events()
        # self.sync_services_usecase.sync()
        # self.db.get()

        # namespaces = self.namespaces_repo.list(filter=Namespace(name="ru", active=True, gitlab=Gitlab(token="4444")))
        # a=self.excels.add_batch_uids("C:/Users/Admin/Documents/Работа/equifax/юрлица/ОсОО МКК М Булак 4 договора/ОсОО МКК М Булак")
        # self.pw.write_to_file(rewrite=True,
        #                       batch=Batch(date=datetime.now(), name="47L_FCH_20230904_0001", id=1,
        #                                   src_file="C:/Users/Admin/IdeaProjects/equifax-sync/equifax-sync-1.0.0/work/dev/requests/Шаблон 4 0 ЮЛ событие 1 1 НКО М Булак.xlsx"))
        self.logger = self.logger_service.get_file_logger("exchange")
        self.server.start()
