# Database Loader
`database_loader` is a module to load information to a database table.
It identify the field from the header fields, so those fields are used to map the table columns 


## Supported Databases:
 - Oracle


## Formats supported:
 - EXCEL
 - CSV
 - TSV


## Instalation
You can install database_loader  by cloning this Git repository
```shell script
$ python -m pip install pip install git+https://github.com/marinellirubens/database_loader#egg=database_loader==1.0.13
```

In order for database_loader to work you will have to install the appropriate database driver.

- Oracle: cx-Oracle version 7.0.0+

You can install this drivers via ``pip``:

    $ python3 -m pip install cx-Oracle

## Usage
```console
$ python -m database_loader -h
usage: __main__.py [-h] [-c COMMIT] [-t TABLE] [-v] [-l] [-d DATABASE] [-f FILE_LOAD] [-u USER] [-p PASSWORD]
                   [-T TYPE] [-V]

Parses command.

optional arguments:
  -h, --help            show this help message and exit
  -c COMMIT, --commit COMMIT
                        Commit every X lines.
  -t TABLE, --table TABLE
                        Table name.
  -v, --verbose         Prints information.
  -l, --clean           Clean table before inserts.
  -d DATABASE, --database DATABASE
                        Database TNS.
  -f FILE_LOAD, --file_load FILE_LOAD
                        File to be load on the table
  -u USER, --user USER  Database User
  -p PASSWORD, --password PASSWORD
                        Database Password
  -T TYPE, --type TYPE  Types CSV, EXCEL, TSV
  -V, --version         Show version
  -B DATABASE_TYPE, --database_type DATABASE_TYPE
                        Database type [ORACLE, MYSQL]
  -C CONNECTION_TYPE, --connection_type CONNECTION_TYPE
                        Connection type [TNS, STRING]
  -H HOST, --host HOST  Database host
  -P PORT, --port PORT  Database port

Process finished with exit code 0
```

## How to use database_loader
### Loading files on database 

