from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from abc import ABC, abstractmethod
from enum import Enum


class ConnectionType(Enum):
    """Enum with the connection types [TNS, STRING]"""
    TNS = 'TNS'
    STRING = 'STRING'


class SelectDatabase(Enum):
    """Enum with the database connection types [ORACLE, MYSQL]"""
    ORACLE = 'OracleDatabase()'
    MYSQL = 'MysqlDatabase()'


class Database(ABC):
    """Database adaptor abstract class"""

    def __init__(self):
        self.cursor = None

    def set_connection_by_tns(self, *args, **kargs):
        """set the connection by TNS (Only works on Oracle),
        returns error if this method is not implemented"""
        raise Exception('Connection type not supported on that database')

    def set_connection_by_connection_string(self, *args, **kargs):
        """set the connection by connection string, returns error
        if this method is not implemented"""
        raise Exception('Connection type not supported on that database')

    @abstractmethod
    def get_cursor(self):
        """Abstract method to return a cursor"""
        pass


class Cursor(ABC):
    """Cursor to execute queries and commands, this class is and
    abstraction and should be implemented on the classes that inherits

    :param database: Database connection to interact with the database
    :type database: Database
    :param table_name: Name of the table that should be loaded
    :type table_name: str
    :param columns: Columns extracted from the file that will be loaed
    :type columns: tuple
    """
    def __init__(self, database: Database = None, table_name: str = None,
                 columns: tuple = None):
        self.database = database
        self.table_name = table_name
        self.columns = columns

    @abstractmethod
    def execute_command(self):
        """Abstract method to execute a command on the database"""
        pass

    @abstractmethod
    def executemany_inserts(self, sql_string: str, values: list):
        """Abstract method to execute many inserts  on the database
        :param sql_string: command to be executed on the database
        :type sql_string: str
        :param values: values to be used on inserts,
            list of tuples ex.: [(1,2,3), (2,3,4)]
        :type values: list
        """
        pass

    @abstractmethod
    def build_sql_template(self):
        """Abstract method to build the insert template for insertion"""
        pass

    def clean_table(self):
        """Cleans table before inserts"""
        self.cursor.execute(f'truncate table {self.table_name}')

    def close(self):
        """Closes the database connection"""
        self.database.close()


class OracleDatabase(Database):
    """Class to connect on the Oracle database inherits from Database"""

    def __init__(self):
        super().__init__()
        exec('import cx_Oracle')
        self.database = eval('cx_Oracle')
        # self.cursor = Cursor()

    def set_connection_by_tns(self, tns: str, user: str, password: str):
        """Set the connection with and Oracle database using the TNSNAMES file

        :param tns: tns name setted on the TNSNAMES.ora
        :type tns: str
        :param user: Database user
        :type user:str
        :param password: Database Password
        :type password: str
        """
        self.user = user
        self.tns = tns
        self.database.connect(self.user, password, self.tns, encoding="UTF-8")
        self.connection = self.database.connect(self.user, password, self.tns,
                                                encoding="UTF-8")

    def set_connection_by_connection_string(self, user: str, password: str,
                                            host: str, port: str,
                                            service_name: str):
        """Set connection by connection string

        :param user: Database user name
        :type user: str
        :param password: Database password
        :type password: str
        :param host: Database host ip
        :type host: str
        :param port: Database port
        :type port: str
        :param service_name: service name
        :type service_name: str
        """
        self.user = user

        tsn = self.database.makedsn(host, port, service_name=service_name)
        self.tns = tsn
        self.database.connect(self.user, password, self.tns, encoding="UTF-8")
        self.connection = self.database.connect(self.user, password,
                                                self.tns, encoding="UTF-8")

    def get_cursor(self, table_name: str, columns: tuple):
        """Returns an Oracle cursor to interact with Oracle database

        :param table_name: Table name
        :type table_name:  str
        :param columns: Column names
        :type columns: tuple
        :return: an oracle cursor
        :rtype: OracleCursor
        """
        self.cursor = OracleCursor(self.connection, table_name, columns)
        self.cursor.build_sql_template()
        return self.cursor


class OracleCursor(Cursor):
    """Class to interact with the Oracle database

    :param database: Database connection to interact with the Oracle database
    :type database: OracleDatabase
    :param table_name: Name of the table
    :type table_name: str
    :param columns: Column names
    :type columns: tuple
    :param error_file: Name of the file to save error logs
    :type error_file: str
    """
    def __init__(self, database: OracleDatabase, table_name: str,
                 columns: tuple):
        super().__init__(database, table_name, columns)
        self.cursor = self.database.cursor()
        self.columns_str = ''
        self.sql_template = ''
        self.error_file = f'{table_name}_{error_file}.log'

    def build_sql_template(self):
        """Build the sql template to do the inserts on the database"""
        values_template = ''
        for index, column in enumerate(self.columns):
            values_template += f':{index + 1}, '
        values_template = values_template[:-2]

        self.columns_str = self.columns_str.replace(',)', ')')
        self.columns_str = str(self.columns).replace("'", '"')

        self.sql_template = f'insert into {self.table_name} ' + \
            '{self.columns_str} values ({values_template})'

    def execute_command(self, sql_string: str):
        """Executes a command on the database

        :param sql_string: Command to be executed on the database
        :type sql_string: str
        """
        self.cursor.execute(sql_string)
        # TODO: Include errors treatment and log

    def write_errors_log(self, offset, error_message):
        """

        :param offset:
        :param error_message:
        """
        with open(self.error_file, 'w+') as log_file:
            log_file.write(f'Row {offset}  has error  {error_message}')

    def executemany_inserts(self, values: list):
        """Execute many inserts on the database

        :param values: Values to be used on the inserts
        :type values: list
        """
        self.cursor.executemany(self.sql_template, values, batcherrors=True)
        batch_errors = self.cursor.getbatcherrors()
        for errorObj in batch_errors:
            self.write_errors_log(errorObj.offset, errorObj.message)


class MysqlDatabase(Database):
    """Class to connect on the Mysql database inherits from Database"""

    def __init__(self):
        super().__init__()
        exec('import mysql.connector')
        self.database = eval('mysql.connector')

    def set_connection_by_connection_string(
        self, user: str, password: str,
        host: str, port: str, service_name: str
    ):
        """Set connection by connection string

        :param user: Database user name
        :type user: str
        :param password: Database password
        :type password: str
        :param host: Database host ip
        :type host: str
        :param port: Database port
        :type port: str
        :param service_name: service name
        :type service_name: str
        """
        self.connection = self.database.connect(host=host,
                                                database=service_name,
                                                user=user,
                                                password=password)
        self.user = user
        self.host = host

    def get_cursor(self, table_name: str, columns: tuple):
        """Returns an Mysql cursor to interact with Mysql database

        :param table_name: Table name
        :type table_name:  str
        :param columns: Column names
        :type columns: tuple
        :return: an Mysql cursor
        :rtype: MysqlCursor
        """
        self.cursor = MysqlCursor(self.connection, table_name, columns)
        self.cursor.build_sql_template()
        return self.cursor


class MysqlCursor(Cursor):
    """Class to interact with the Mysql database

    :param database: Database connection to interact with the Oracle database
    :type database: MysqlDatabase
    :param table_name: Name of the table
    :type table_name: str
    :param columns: Column names
    :type columns: tuple
    :param error_file: Name of the file to save error logs
    :type error_file: str
    """
    def __init__(self, database: MysqlDatabase,
                 table_name: str, columns: tuple):
        super().__init__(database, table_name, columns)
        self.cursor = self.database.cursor()
        self.columns_str = ''
        self.error_file = error_file

    def build_sql_template(self):
        """Build the sql template to do the inserts on the database"""
        values_template = ''
        for index, column in enumerate(self.columns):
            values_template += f'%s, '
        values_template = values_template[:-2]
        self.columns_str = str(self.columns).replace("'", '')
        self.columns_str = self.columns_str.replace(',)', ')')
        self.sql_template = f'insert into {self.table_name} ' + \
            '{self.columns_str} values ({values_template})'

    def execute_command(self, sql_string: str):
        """Executes a command on the database

        :param sql_string: Command to be executed on the database
        :type sql_string: str
        """
        self.cursor.execute(sql_string)

    def executemany_inserts(self, values: tuple):
        """Execute many inserts on the database

        :param values: Values to be used on the inserts
        :type values: list
        """
        self.cursor.executemany(self.sql_template, values)
