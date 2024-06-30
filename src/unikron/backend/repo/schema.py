import inspect
from dataclasses import dataclass

from peewee import *

from src.mybootstrap_core_itskovichanton.orm import entity
from src.mybootstrap_core_itskovichanton.utils import hashed
from src.mybootstrap_pyauth_itskovichanton.entities import User

from src.unikron.backend.entity.common import UserStatus, UserPermission, Country, Service, ServiceCategory, AuditMsg

database = PostgresqlDatabase('unikron', **{'host': 'localhost', 'port': 3, 'user': 'postgres', 'password': '92559255'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


@entity(ServiceCategory)
class ServiceCategoryM(BaseModel):
    id = BigAutoField()
    name = CharField(unique=True)

    class Meta:
        table_name = 'category'


@entity(Country)
class CountryM(BaseModel):
    id = BigAutoField()
    name = CharField(unique=True)
    strid = CharField(null=True, unique=True)

    class Meta:
        table_name = 'country'


@entity(UserPermission)
class DictUserPermissionM(BaseModel):
    id = BigAutoField()
    name = CharField(unique=True)

    class Meta:
        table_name = 'dict_user_permission'


@entity(UserStatus)
class DictUserStatusM(BaseModel):
    id = BigAutoField()
    name = CharField(unique=True)

    class Meta:
        table_name = 'dict_user_status'


@entity(Service)
class ServiceM(BaseModel):
    id = BigAutoField()
    category = ForeignKeyField(column_name='category_id', field='id', model=ServiceCategoryM)
    cherkizon_service = CharField(null=True)
    country = ForeignKeyField(column_name='country_id', field='id', model=CountryM)
    created_at = DateField()
    description = CharField(null=True)
    gitlab_project_id = IntegerField(unique=True)
    gitlab_url = CharField(unique=True)
    longread = TextField(null=True)
    name = CharField(unique=True)
    tags = CharField(null=True)
    title = CharField(unique=True)

    @staticmethod
    def get_short_fields():
        return [ServiceM.id, ServiceM.category, ServiceM.cherkizon_service, ServiceM.country, ServiceM.created_at,
                ServiceM.description, ServiceM.title,
                ServiceM.gitlab_url, ServiceM.gitlab_project_id, ServiceM.name, ServiceM.tags, ServiceM.tags]

    class Meta:
        table_name = 'service'


@entity(User)
class UserM(BaseModel):
    id = BigAutoField()
    additional_contact = CharField(null=True, unique=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")], null=True)
    deleted_at = DateTimeField(null=True)
    email = CharField(unique=True)
    name = CharField()
    password = CharField()
    role = CharField(null=True)
    status = ForeignKeyField(column_name='status_id', constraints=[SQL("DEFAULT 1")], field='id', model=DictUserStatusM)
    username = CharField(unique=True)
    telegram_username = CharField()

    @staticmethod
    def get_public_fields():
        return [UserM.id, UserM.additional_contact, UserM.created_at, UserM.deleted_at, UserM.email, UserM.name,
                UserM.role, UserM.status, UserM.username, UserM.telegram_username]

    class Meta:
        table_name = 'user'


class UserPermissionM(BaseModel):
    permission_id = IntegerField()
    user_id = IntegerField()

    class Meta:
        table_name = 'user_permission'
        primary_key = False


@hashed
@dataclass
class _UserServiceRole:
    user: User = None
    role: str = None


@entity(_UserServiceRole)
class UserServiceRolesM(BaseModel):
    service_id = IntegerField(null=True)
    user_id = IntegerField(null=True)
    user_role = CharField()

    class Meta:
        table_name = 'user_service_roles'
        primary_key = False


@entity(AuditMsg)
class AuditMsgM(BaseModel):
    id = BigAutoField()
    message = CharField(null=True)
    hook = CharField(null=True)
    time = DateTimeField(constraints=[SQL("DEFAULT now()")], null=True)

    class Meta:
        table_name = 'audit'
