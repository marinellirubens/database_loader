# Database Loader
`database_loader` is a module to load information to a database table.
It identify the field from the header fields, so those fields are used to map the table columns 


## Supported Databases:
 - Oracle
 - MySql


## Formats supported:
 - EXCEL
 - CSV
 - TSV


## Instalation
You can install database_loader  by cloning this Git repository
```shell script
$ python -m pip install git+https://github.com/marinellirubens/database_loader#egg=database_loader==1.0.33
```

In order for database_loader to work you will have to install the appropriate database driver.

- Oracle: cx-Oracle version 7.0.0+
- Mysql: mysql-connector-python version 8.0.0+

You can install this drivers via ``pip``:
```console
$ python -m pip install cx-Oracle
$ python -m pip install mysql-connector-python
````

## Usage
```console
$ database_loader -h
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
### Check Version
```console
$ database_loader --version
databaseloader version: 1.0.33
```

#### Loading files on database by TNSNAMES(ORACLE Only)
Executed on `windows`
```console
$ database_loader --database TESTDB ^
                  --user root ^
                  --password"123456" ^
                  --table tb_salary ^
                  --file C:\insert_files\insert.tsv ^
                  --commit 5000 ^
                  --type TSV ^
                  --database_type ORACLE ^
                  --connection_type TNS ^
                  --clean
```

Executed on `linux`  
```console
$ database_loader --database TESTDB \
                  --user root \
                  --password"123456" \
                  --table tb_salary \
                  --file C:\insert_files\insert.tsv \
                  --commit 5000 \
                  --type TSV \
                  --database_type ORACLE \
                  --connection_type TNS \
                  --clean
```


#### Loading files on Oracle database by Connection String
Executed on `windows`
```console
$ database_loader --connection STRING ^
                  --database TESTDB ^
                  --host 192.168.15.168 ^
                  --port 1601 ^
                  --user root ^
                  --password"123456" ^
                  --database_type ORACLE ^
                  --table tb_salary ^
                  --file C:\insert_files\insert.tsv ^
                  --commit 5000 ^
                  --type TSV ^
                  --clean
```

Executed on `linux`  
```console
$ database_loader --connection STRING \
                  --database TESTDB \
                  --host 192.168.15.168 \
                  --port 1601 \
                  --user root \
                  --database_type ORACLE \
                  --password"123456" \
                  --table tb_salary \
                  --file /insert_files/insert.tsv \
                  --commit 5000 \
                  --type TSV \
                  --clean
```
