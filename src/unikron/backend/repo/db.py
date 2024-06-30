from dataclasses import dataclass
from typing import Protocol

import psycopg2
from paprika import singleton
from peewee import PostgresqlDatabase
from src.mybootstrap_ioc_itskovichanton.ioc import bean


class DB(Protocol):

    def get(self) -> PostgresqlDatabase:
        ...

    def get_psycopg2_connection(self):
        ...

    def exec_sql(self, query, params) -> list[dict]:
        ...


@dataclass
class _Config:
    user: str
    password: str
    host: str = "localhost"
    port: int = 5432


@bean(cfg=("db", _Config))
class DBImpl(DB):

    @singleton
    def get(self) -> PostgresqlDatabase:
        return PostgresqlDatabase('unikron', **self.cfg.__dict__)

    @singleton
    def get_psycopg2_connection(self):
        return psycopg2.connect(dbname='unikron', **self.cfg.__dict__)

    def exec_sql(self, query, params) -> list[dict]:
        result = []
        qr = self.get().execute_sql(sql=query, params=params)
        for r in qr:
            row = {}
            for i in range(len(qr.description)):
                row[qr.description[i].name] = r[i]
            result.append(row)
        return result
