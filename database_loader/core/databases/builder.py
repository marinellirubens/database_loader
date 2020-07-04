from enum import Enum

class Database(Enum):
    ORACLE = 'ORACLE'
    MYSQL = 'MYSQL'

class ConnectionType(Enum):
    DNS = 'DNS'
    CONNECTION_STRING = 'STRING'

class DabaseBuilder:
    def __init__(self):
        pass

    def set_database_type(self, database_type: Database = Database.ORACLE):
        pass

    def set_conection_type(self, connection_type: ConnectionType = ConnectionType.CONNECTION_STRING):
        pass

    def set_query_string(self, database_name: str, user: str, password, host: str, port: str):
        pass

    def set_dns_info(self, database_name: str, user: str, password):
        pass

    def build(self):
        return None