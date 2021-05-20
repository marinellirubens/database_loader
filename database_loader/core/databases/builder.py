"""Module to contain the Builder used for the database connection"""
from __future__ import (absolute_import, division, print_function)

from database_loader.core.databases.database import SelectDatabase
from database_loader.core.databases.database import ConnectionType
from database_loader.core.databases.database import Database
from database_loader.core.databases.database import OracleDatabase
from database_loader.core.databases.database import MysqlDatabase
from database_loader.core.databases.database import Cursor


class CursorBuilder:
    """Builder of the database classes"""
    def __init__(self):
        self.connection_type = ConnectionType.STRING
        self.database = eval(SelectDatabase.ORACLE.value)
        self.database_name = ''
        self.user = ''
        self.password = ''
        self.host = ''
        self.port = ''
        self.table_name = ''
        self.columns = tuple()

    def set_database_type(self, database: SelectDatabase = SelectDatabase.ORACLE):
        """Set the database connection type

        :param database: Database connection
        :type database: SelectDatabase
        :return: returns self
        :rtype: CursorBuilder
        """
        self.database = eval(database.value)
        return self

    def set_connection_type(
        self, connection_type: ConnectionType = ConnectionType.STRING
    ):
        """

        :param connection_type: String with the connection type
        :type connection_type: ConnectionType
        :return: returns self
        :rtype: CursorBuilder
        """
        self.connection_type = connection_type.value
        return self

    def set_connection_string(self, database_name: str, user: str, password, host: str, port: str):
        """Sets the connection string for the correct type of connection

        :param database_name: Name of the database that will be used
        :type database_name: str
        :param user: Name of the user
        :type user: str
        :param password: Password for the informed user
        :type password: str
        :param host: Host name or ip address
        :type host: str
        :param port: Hots port used for the database
        :type port: str
        :return: returns self
        :rtype: CursorBuilder
        """
        if self.connection_type == ConnectionType.STRING.value:
            self.set_query_string(database_name, user, password, host, port)
        else:
            self.set_tns_info(database_name, user, password)
        return self

    def set_query_string(self, database_name: str, user: str, password, host: str, port: str):
        """Sets the info used when the connection is by query string

        :param database_name: Name of the database that will be used
        :type database_name: str
        :param user: Name of the user
        :type user: str
        :param password: Password for the informed user
        :type password: str
        :param host: Host name or ip address
        :type host: str
        :param port: Hots port used for the database
        :type port: str
        :return: returns self
        :rtype: CursorBuilder
        """
        self.database_name = database_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        return self

    def set_tns_info(self, database_name: str, user: str, password):
        """Sets the info for the connection when the connection method is TNS

        :param database_name: Name of the database that will be used
        :type database_name: str
        :param user: Name of the user
        :type user: str
        :param password: Password for the informed user
        :type password: str
        :return: returns self
        :rtype: CursorBuilder
        """
        self.database_name = database_name
        self.user = user
        self.password = password
        return self

    def set_table_info(self, table_name: str, columns: tuple):
        """Sets the table info used by the cursor

        :param table_name: Name of the table to be uploaded
        :type table_name: str
        :param columns: List of the columns used to build the insert command
        :type columns: tuple
        :return: returns self
        :rtype: CursorBuilder
        """
        self.table_name = table_name
        self.columns = columns
        return self

    def build(self):
        """Returns a cursor to interact with the database selected using the parameters
        set on the other methods of this class

        :return: a cursor to interact with the database
        :rtype: Cursor
        """
        if self.connection_type == ConnectionType.TNS.value:
            self.database.set_connection_by_tns(
                self.database_name, self.user, self.password)
        else:
            self.database.set_connection_by_connection_string(self.user, self.password, self.host,
                                                              self.port, self.database_name)
        return self.database.get_cursor(self.table_name, self.columns)
