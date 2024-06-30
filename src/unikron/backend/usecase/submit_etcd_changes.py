from typing import Protocol

from src.mybootstrap_core_itskovichanton.realtime_config import RealTimeConfigManager
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_mvc_itskovichanton.exceptions import CoreException, \
    ERR_REASON_SERVER_RESPONDED_WITH_ERROR_NOT_FOUND
from src.mybootstrap_pyauth_itskovichanton.entities import Session
from src.mybootstrap_pyauth_itskovichanton.frontend.controller import GetUserAction, GetUserActionParams

from src.unikron.backend.apis.cherkizon import Cherkizon
from src.unikron.backend.apis.replicas import Replicas
from src.unikron.backend.entity.common import SearchServiceQuery, Service, USER_PERMISSION_CONTROL_SERVICE, \
    USER_PERMISSION_READ_SERVICE, USER_PERMISSION_READ_DEPLOYS, Deploy, USER_PERMISSION_READ_ETCDS, DeployQuery, \
    USER_PERMISSION_WRITE_ETCDS
from src.unikron.backend.repo.service import ServiceRepo
from src.unikron.backend.usecase.check_account_permission import CheckAccountPermissionUseCase
from src.unikron.backend.usecase.search_deploys import SearchDeploysUseCase


class SubmitETCDChangesUseCase(Protocol):

    def submit(self, session: Session, filter: Deploy, data: dict):
        ...


@bean
class SubmitETCDChangesUseCaseImpl(SubmitETCDChangesUseCase):
    check_permissions_uc: CheckAccountPermissionUseCase
    search_deploys_uc: SearchDeploysUseCase
    get_user_action: GetUserAction
    real_time_cfg_mgr: RealTimeConfigManager
    replicas: Replicas

    def submit(self, session: Session, filter: Deploy, data: dict):
        session = self.get_user_action.run(session)
        self.check_permissions_uc.check_permission(session, USER_PERMISSION_WRITE_ETCDS)
        listing = self.search_deploys_uc.search_one(session, filter)
        deploy = listing.deploys[0]
        machine = listing.machines[deploy.machine]
        replica_etcds = self.replicas.list_etcds(deploy.internal_url)
        for key, value in data.items():
            self.real_time_cfg_mgr.put(key, value, machine.ip, machine.etcd_port, key_prefix=replica_etcds.key_prefix)
