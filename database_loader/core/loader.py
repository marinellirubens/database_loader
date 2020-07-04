"""Module to load data"""
import os
import argparse
import sys
from enum import Enum
import pandas
import numpy
import cx_Oracle

# import sqlalchemy
import pkg_resources  # part of setuptools

class ReaderType(Enum):
    """Enum to contain the reader types"""
    TSV = pandas.read_table
    CSV = pandas.read_csv
    EXCEL = pandas.read_excel


class Loader:
    """Class to load the file into database(oracle)

    :param commit_amount: Amount of lines that will be commit each time
    :param table_name: table name
    :param printer: defines if information will be printed
    :param clean_table: defines if cleans tables before inserts
    :param database: the TNS of the databases
    :param user: user name
    :param password: user password
    """
    def __init__(self, commit_amount: int = 1000, table_name: str = '', printer: bool = False,
                 clean_table: bool = False, database: str = None, user: str = None, password: str = None):
        self.commit_amount = commit_amount
        self.table_name = table_name
        self.printer = printer
        self.clean = clean_table
        self.data_frame = None
        self.dns = database
        self.user = user
        self.password = password

    def read_file(self, file_name, directory='.', reader=ReaderType.TSV):
        """Reads the file content"""
        file_path = os.path.join(directory, file_name)
        self.data_frame = reader(file_path).replace(to_replace=numpy.nan, value='')

    def get_conection(self):
        """Returns the connection with oracle"""
        # dsn = cx_Oracle.makedsn("204.79.148.141", 1526, service_name="BRTMSP")
        # connection = cx_Oracle.connect("tms_if", "mgri2tmbr", dsn, encoding="UTF-8")
        return cx_Oracle.connect(self.user, self.password, self.dns, encoding="UTF-8")

    def clean_table(self):
        """Wipes the data from the table"""
        connection = self.get_conection()
        cursor = connection.cursor()
        cursor.execute(f'truncate table {self.table_name}')
        connection.close()

    def load_into_database(self):
        """Loads the information into the table"""
        if self.clean:
            self.clean_table()

        connection = self.get_conection()
        cursor = connection.cursor()
        columns = tuple(self.data_frame.columns.values)
        columns_str = str(columns).replace("'", '')
        insert_sql = 'insert all\n'

        for index, row in self.data_frame.iterrows():
            values = []
            for column_name in columns:
                values.append(row[column_name])

            insert_sql += f'into {self.table_name} {columns_str} values {tuple(values)}\n'

            if (index + 1) % self.commit_amount == 0 and index > 0:
                if self.printer:
                    print(f'Inseridos {index + 1} registros na tabela {self.table_name}')

                insert_sql += f'select * from dual'
                cursor.execute(insert_sql)
                cursor.execute("commit")
                insert_sql = 'insert all\n'
            # break
        if insert_sql != 'insert all\n':
            insert_sql += f'select * from dual'
            cursor.execute(insert_sql)
            cursor.execute("commit")
        connection.close()


def get_arguments(args: list = sys.argv[1:]):
    """Parse argument on command line execution

    :param args: arguments to be parsed
    :return: returns the options parsed
    """
    parser = argparse.ArgumentParser(description='Parses command.')
    parser.add_argument('-c', '--commit', help='Commit every X lines.', action='store', type=str, default=500)
    parser.add_argument('-t', '--table', help='Table name.', action='store', type=str)
    parser.add_argument('-v', '--verbose', help='Prints information.', action='store_true')
    parser.add_argument('-l', '--clean', help='Clean table before inserts.', action='store_true')
    parser.add_argument('-d', '--database', help='Database TNS.', action='store', type=str)
    parser.add_argument('-f', '--file_load', help='File to be load on the table', action='store', type=str)
    parser.add_argument('-u', '--user', help='Database User', action='store', type=str)
    parser.add_argument('-p', '--password', help='Database Password', action='store', type=str)
    parser.add_argument('-T', '--type', help='Types CSV, EXCEL, TSV', action='store', type=str)
    parser.add_argument('-V', '--version', help='Types CSV, EXCEL, TSV', action='store_true')
    options = parser.parse_args(args)
    return options


def print_version():
    version = pkg_resources.require("databaseloader")[0].version
    print(f'databaseloader version: {version}')
    exit(0)


def main():
    """Main method for the insert"""
    options = get_arguments(sys.argv[1:])

    if options.version:
        print_version()
    print(options.type)
    # os.chdir('C:\RBS\RBS\Chamados\TMS\IBATMS-1868')
    #  -t tmp_rbs_occur_sem_canhoto -d oracle -f C:\RBS\RBS\Chamados\TMS\IBATMS-1868\insert.tsv
    loader = Loader(options.commit, table_name=options.table, printer=options.verbose, clean_table=options.clean, database=options.database, user=options.user, password=options.password)
    loader.read_file(file_name=options.file_load, readertype=eval(f'ReaderType.{options.type}'))
    loader.load_into_database()


if __name__ == '__main__':
    main()