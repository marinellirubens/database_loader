from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from database_loader.core.databases.database import SelectDatabase, ConnectionType, Database


class CursorBuilder:
    def __init__(self):
        pass

    def set_database_type(self, database: Database = SelectDatabase.ORACLE):
        """

        :param database:
        """
        self.database = eval(database.value)
        return self

    def set_connection_type(self, connection_type: ConnectionType = ConnectionType.CONNECTION_STRING):
        """

        :param connection_type:
        """
        self.connection_type = connection_type.value
        return self

    def set_connection_string(self, database_name: str, user: str, password, host: str, port: str):
        if self.connection_type == ConnectionType.TNS.value:
            self.set_query_string(database_name, user, password, host, port)
        else:
            self.set_tns_info(database_name, user, password)
        return self

    def set_query_string(self, database_name: str, user: str, password, host: str, port: str):
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
        self.table_name = table_name
        self.columns = columns
        return self

    def build(self):
        if self.connection_type == ConnectionType.TNS.value:
            self.database.set_connection_by_tns(self.database_name, self.user, self.password)
        else:
            self.database.set_connection_by_connection_string(self.user, self.password, self.host, self.host, self.database_name)
        return self.database.get_cursor(self.table_name, self.columns)