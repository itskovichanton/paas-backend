from peewee import *
from src.mybootstrap_core_itskovichanton.orm import entity
from src.mybootstrap_pyauth_itskovichanton.entities import User

from src.unikron.backend.entity.common import UserStatus, UserPermission

database = PostgresqlDatabase('unikron', **{'host': 'localhost', 'port': 3, 'user': 'postgres', 'password': '92559255'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    id = BigAutoField()

    class Meta:
        database = database


class CategoryM(BaseModel):
    id = BigAutoField()
    name = CharField(unique=True)

    class Meta:
        table_name = 'category'


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


class ServiceM(BaseModel):
    id = BigAutoField()
    category_id = IntegerField()
    cherkizon_service = CharField(null=True)
    country_id = IntegerField(null=True)
    created_at = DateField()
    description = CharField(null=True)
    gitlab_id = IntegerField(unique=True)
    gitlab_url = CharField(unique=True)
    longread = TextField(null=True)
    name = CharField(unique=True)
    tags = CharField(null=True)
    title = CharField(unique=True)

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

    class Meta:
        table_name = 'user'


class UserPermissionM(BaseModel):
    permission_id = IntegerField()
    user_id = IntegerField()

    class Meta:
        table_name = 'user_permission'
        primary_key = False


class UserServiceRolesM(BaseModel):
    service_id = IntegerField(null=True)
    user_id = IntegerField(null=True)
    user_role = CharField()

    class Meta:
        table_name = 'user_service_roles'
        primary_key = False
