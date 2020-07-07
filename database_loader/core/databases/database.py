from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from abc import ABC, abstractmethod, abstractproperty
from enum import Enum


class ConnectionType(Enum):
    TNS = 'TNS'
    CONNECTION_STRING = 'STRING'


class Database(ABC):
    def __init__(self):
        self.cursor = Cursor(self, None, None)

    def set_connection_by_tns(self, *args, **kargs):
        """

        :param args:
        :param kargs:
        """
        raise Exception('Connection type not supported on that database')

    def set_connection_by_connection_string(self, *args, **kargs):
        raise Exception('Connection type not supported on that database')

    @abstractmethod
    def get_cursor(self):
        pass


class Cursor:
    def __init__(self, database: Database = None, table_name: str = None, columns: tuple = None):
        self.database = database
        self.table_name = table_name
        self.columns = columns

    @abstractmethod
    def execute_command(self, sql_string: str):
        pass

    @abstractmethod
    def executemany_inserts(self, sql_string: str, values: tuple):
        pass

    @abstractmethod
    def build_sql_template(self, table_name: str, columns: tuple):
        pass

    def clean_table(self):
        self.cursor.execute(f'truncate table {self.table_name}')

    def close(self):
        self.database.close()


class OracleDatabase(Database):
    def __init__(self):
        super().__init__()
        exec('import cx_Oracle')
        self.database = eval('cx_Oracle')
        self.cursor = Cursor()

    def set_connection_by_tns(self, tns: str, user: str, password: str):
        self.user = user
        self.tns = tns
        self.database.connect(self.user, password, self.tns, encoding="UTF-8")
        self.connection = self.database.connect(self.user, password, self.tns, encoding="UTF-8")

    def set_connection_by_connection_string(self, user: str, password: str, host: str, port: str, service_name):
        self.user = user

        tsn = self.database.makedsn(host, port, service_name=service_name)
        self.tns = tsn
        self.database.connect(self.user, password, self.tns, encoding="UTF-8")
        self.connection = self.database.connect(self.user, password, self.tns, encoding="UTF-8")

    def get_cursor(self, table_name: str, columns: tuple):
        self.cursor = OracleCursor(self.connection, table_name, columns)
        self.cursor.build_sql_template()
        return self.cursor



class OracleCursor(Cursor):
    def __init__(self, database: OracleDatabase, table_name: str, columns: tuple):
        super().__init__(database, table_name, columns)
        self.cursor = self.database.cursor()

    def build_sql_template(self):
        values_template = ''
        for index, column in enumerate(self.columns):
            values_template += f':{index + 1}, '
        values_template = values_template[:-2]
        self.columns_str = self.columns_str.replace(',)', ')')
        self.columns_str = str(self.columns).replace("'", '"')

        self.sql_template = f'insert into {self.table_name} {self.columns_str} values ({values_template})'

    def execute_command(self, sql_string: str):
        self.cursor.execute(sql_string)

    def executemany_inserts(self, values: list):
        self.cursor.executemany(self.sql_template, values)

    def clean_table(self):
        self.cursor.execute(f'truncate table {self.table_name}')

class MysqlDatabase(Database):
    def __init__(self):
        super().__init__()
        exec('import mysql.connector')
        self.database = eval('mysql.connector')

    def set_connection_by_connection_string(self, user: str, password: str, host: str, port: str, service_name: str):
        self.connection = self.database.connect(host=host,
                                                database=service_name,
                                                user=user,
                                                password=password)
        self.user = user
        self.host = host

    def get_cursor(self, table_name: str, columns: tuple):
        self.cursor = MysqlCursor(self.connection, table_name, columns)
        self.cursor.build_sql_template()
        return self.cursor


class MysqlCursor(Cursor):
    def __init__(self, database: MysqlDatabase, table_name: str, columns: tuple):
        super().__init__(database, table_name, columns)
        self.cursor = self.database.cursor()

    def build_sql_template(self):
        values_template = ''
        for index, column in enumerate(self.columns):
            values_template += f'%s, '
        values_template = values_template[:-2]
        self.columns_str = str(self.columns).replace("'", '')
        self.columns_str = self.columns_str.replace(',)', ')')
        self.sql_template = f'insert into {self.table_name} {self.columns_str} values ({values_template})'

    def execute_command(self, sql_string: str):
        self.cursor.execute(sql_string)

    def executemany_inserts(self, values: tuple):
        self.cursor.executemany(self.sql_template, values)


class SelectDatabase(Enum):
    ORACLE = 'OracleDatabase()'
    MYSQL = 'MysqlDatabase()'
