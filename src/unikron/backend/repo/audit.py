import datetime
import json
from typing import Protocol

from src.mybootstrap_core_itskovichanton.orm import infer_where, to_real_entity
from src.mybootstrap_core_itskovichanton.utils import silent_catch
from src.mybootstrap_ioc_itskovichanton.ioc import bean
from src.mybootstrap_pyauth_itskovichanton.backend.user_repo import UserRepo
from src.mybootstrap_pyauth_itskovichanton.entities import User, Session

from src.unikron.backend.entity.common import AuditMsg, Deploy, Service
from src.unikron.backend.repo.db import DB
from src.unikron.backend.repo.schema import AuditMsgM


class AuditRepo(Protocol):

    def save(self, a: AuditMsg) -> bool:
        ...


@bean
class AuditRepoImpl(AuditRepo):

    def _preprocess_hook(self, a):
        if type(a) == Session:
            a = a.account
        if type(a) == User:
            a = {"username": a.username, "name": a.name, "id": a.id, "ip": a.ip}
        if type(a) == Deploy:
            a = {"systemd": a.systemd_name}
        if type(a) == Service:
            a = {"name": a.name, "id": a.id}
        return a

    @to_real_entity
    def search(self, a: AuditMsg):
        return (AuditMsgM.select(AuditMsgM)
                .where(AuditMsgM.message << a.message))

    @silent_catch
    def save(self, a: AuditMsg):
        a.message = self._compile_msg_prefix(a) + " " + a.message
        a.hook = {hook_name: self._preprocess_hook(hook_value) for hook_name, hook_value in a.hook.items()}
        return (AuditMsgM(message=a.message, hook=json.dumps(a.hook), time=datetime.datetime.now())
                .save(force_insert=True))

    #
    # @to_real_entity
    # def get_permissions(self, account_id):
    #     return [x.dictAuditm for x in
    #             (AuditM.select(AuditM, DictAuditM)
    #              .join(DictAuditM, on=(DictAuditM.id == AuditM.permission_id))
    #              .where(AuditM.user_id == account_id))]

    def _compile_msg_prefix(self, a: AuditMsg) -> str:
        r = []
        for hn, hv in a.hook.items():
            if hn == "deploy":
                r.append(f"деплой: {hv.name}, {hv.systemd_name}")
            elif hn == "author":
                if type(hv) == Session:
                    hv = hv.account
                if type(hv) == User:
                    r.append(f"автор: {hv.username}, {hv.name}, ip: {hv.ip}")
        return f"[{", ".join(r)}]"
