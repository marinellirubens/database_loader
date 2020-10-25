from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from database_loader.core.databases.database import SelectDatabase
from database_loader.core.databases.database import ConnectionType
from database_loader.core.databases.database import Database
from database_loader.core.databases.database import OracleDatabase
from database_loader.core.databases.database import MysqlDatabase
from database_loader.core.databases.database import Cursor


class CursorBuilder:
    """Builder of the database classes

        Examples:

    """
    def __init__(self):
        pass

    def set_database_type(self, database: Database = SelectDatabase.ORACLE):
        """

        :param database:
        """
        self.database = eval(database.value)
        return self

    def set_connection_type(
        self, connection_type: ConnectionType = ConnectionType.STRING
    ):
        """

        :param connection_type:
        """
        self.connection_type = connection_type.value
        return self

    def set_connection_string(self, database_name: str, user: str, password,
                              host: str, port: str):
        if self.connection_type == ConnectionType.STRING.value:
            self.set_query_string(database_name, user, password, host, port)
        else:
            self.set_tns_info(database_name, user, password)
        return self

    def set_query_string(self, database_name: str, user: str, password,
                         host: str, port: str):
        """

        :param database_name:
        :param user:
        :param password:
        :param host:
        :param port:
        """
        self.database_name = database_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        return self

    def set_tns_info(self, database_name: str, user: str, password):
        """

        :param database_name:
        :param user:
        :param password:
        """
        self.database_name = database_name
        self.user = user
        self.password = password
        return self

    def set_table_info(self, table_name: str, columns: str):
        """

        :param table_name:
        :param columns:
        :return:
        """
        self.table_name = table_name
        self.columns = columns
        return self

    def build(self):
        """

        :return: a cursor to interact with the database
        :rtype: Cursor
        """
        if self.connection_type == ConnectionType.TNS.value:
            self.database.set_connection_by_tns(
                self.database_name, self.user, self.password)
        else:
            self.database.set_connection_by_connection_string(
                self.user, self.password, self.host,
                self.port, self.database_name
            )
        return self.database.get_cursor(self.table_name, self.columns)
