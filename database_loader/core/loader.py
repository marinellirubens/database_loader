"""Module to load data"""
from __future__ import (absolute_import, division, print_function)

import argparse
from argparse import Namespace
import sys
from enum import Enum
import pandas
import numpy
import pkg_resources  # part of setuptools

from database_loader.core.databases.builder import CursorBuilder
from database_loader.core.databases.database import ConnectionType
from database_loader.core.databases.database import SelectDatabase
from database_loader.core.databases.database import ConnectionType
from database_loader.core.databases.database import MysqlDatabase
from database_loader.core.databases.database import OracleDatabase
import pkg_resources  # part of setuptools


class ReaderType(Enum):
    """Enum to contain the reader types"""
    TSV = pandas.read_table
    CSV = pandas.read_csv
    EXCEL = pandas.read_excel


class Loader:
    """Class to load the file into database(oracle)

    :param host: Database host name or ip address
    :type host: str
    :param port: Host port used by the database
    :type port: str
    :param commit_amount: Amount of lines that will be commit each time
    :type commit_amount: int
    :param table_name: table name
    :type table_name: str
    :param printer: defines if information will be printed
    :type printer: bool
    :param clean_table: defines if cleans tables before inserts
    :type clean_table: bool
    :param database: the TNS of the databases
    :type database: str
    :param user: user name
    :type user: str
    :param password: user password
    :type password: str
    :param database_type: database type (ORACLE, MYSQL)
    :type database_type: str
    :param connection_type: Connection type used (TNS, STRING)
    :type connection_type: str
    """

    def __init__(self, host: str = '', port: str = '', commit_amount: int = 1000, table_name: str = '',
                 printer: bool = False, clean_table: bool = False, database: str = None, user: str = None,
                 password: str = None, database_type: str = 'ORACLE', connection_type: str = 'TNS'):
        self.commit_amount = int(commit_amount)
        self.table_name = table_name
        self.printer = printer
        self.clean = clean_table
        self.data_frame = None
        self.tns = database
        self.user = user
        self.password = password
        self.database_type = database_type
        self.connection_type = connection_type
        self.host = host
        self.port = port
        self.columns = tuple()

    def read_file(self, file_name: str, reader: ReaderType = ReaderType.TSV):
        """Reads the file content

        :param file_name: name of the file to be read
        :type file_name: str
        :param reader: Reader method that will be used to read the data from file
        :type reader: ReaderType
        """
        self.data_frame = reader(file_name).replace(to_replace=numpy.nan, value='')
        self.columns = tuple(self.data_frame.columns.values)

    def get_cursor(self):
        """Returns the connection with oracle"""
        connection = eval(f'ConnectionType.{self.connection_type}')
        cursor_builder = CursorBuilder()
        cursor_builder.set_database_type(
            eval(f'SelectDatabase.{self.database_type}'))
        cursor_builder.set_connection_type(connection)
        cursor_builder.set_connection_string(self.tns, self.user,
                                             self.password, self.host,
                                             self.port)

        cursor_builder.set_table_info(self.table_name, self.columns)
        cursor = cursor_builder.build()
        return cursor

    def load_into_database(self):
        """Loads the information into the table"""
        cursor = self.get_cursor()
        if self.clean:
            cursor.clean_table()

        insert_values = []
        for index, row in self.data_frame.iterrows():
            values = []
            for column_name in self.columns:
                values.append(row[column_name])

            insert_values.append(tuple(values))

            if (index + 1) % self.commit_amount == 0 and index > 0:
                cursor.executemany_inserts(insert_values)
                cursor.execute_command("commit")
                insert_values = []
                if self.printer:
                    print(f'{index + 1} lines inserted on table '
                          '{self.table_name}')
            # break
        if insert_values:
            cursor.executemany_inserts(insert_values)
            cursor.execute_command("commit")
            if self.printer:
                print(f'{index + 1} lines inserted on table {self.table_name}')

        cursor.close()
        print(f'Process Finished!')


def get_arguments(args: list = sys.argv[1:]):
    """Parse argument on command line execution

    :param args: arguments to be parsed
    :type args: list
    :return: returns the options parsed
    :rtype: Namespace
    """
    # TODO: Include output errors file parameter
    parser = argparse.ArgumentParser(description='Parses command.')
    parser.add_argument('-c', '--commit', help='Commit every X lines.',
                        action='store', type=int, default=500)

    parser.add_argument('-t', '--table', help='Table name.',
                        action='store', type=str)

    parser.add_argument('-v', '--verbose', help='Prints information.',
                        action='store_true')

    parser.add_argument('-l', '--clean', help='Clean table before inserts.',
                        action='store_true')

    parser.add_argument('-d', '--database', help='Database TNS.',
                        action='store', type=str)

    parser.add_argument('-f', '--file_load',
                        help='File to be load on the table',
                        action='store', type=str)

    parser.add_argument('-u', '--user', help='Database User',
                        action='store', type=str)

    parser.add_argument('-p', '--password', help='Database Password',
                        action='store', type=str)

    parser.add_argument('-T', '--type', help='Types CSV, EXCEL, TSV',
                        action='store', type=str, default="TSV")

    parser.add_argument('-V', '--version', help='Show version',
                        action='store_true')

    parser.add_argument('-B', '--database_type',
                        help='Database type [ORACLE, MYSQL]',
                        action='store', type=str, default="ORACLE")

    parser.add_argument('-C', '--connection_type',
                        help='Connection type [TNS, STRING]',
                        action='store', type=str, default="TNS")

    parser.add_argument('-H', '--host', help='Database host',
                        action='store', type=str)

    parser.add_argument('-P', '--port', help='Database port',
                        action='store', type=str)

    options = parser.parse_args(args)
    return options


def print_version():
    """Prints database_loader version"""
    version = pkg_resources.require("database_loader")[0].version
    print(f'v{version}')
    exit(0)


def main():
    """Main method for the insert"""
    options = get_arguments(sys.argv[1:])
    if options.version:
        print_version()

    loader = Loader(host=options.host,
                    port=options.port,
                    commit_amount=options.commit,
                    table_name=options.table,
                    printer=options.verbose,
                    clean_table=options.clean,
                    database=options.database,
                    user=options.user,
                    password=options.password,
                    database_type=options.database_type,
                    connection_type=options.connection_type)

    loader.read_file(file_name=options.file_load,
                     reader=eval(f'ReaderType.{options.type}'))
    loader.load_into_database()


if __name__ == '__main__':
    main()
