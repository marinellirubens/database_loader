Database Loader
===
`database_loader` is a module to load information to a database table.
It identify the field from the header fields, so those fields are used to map the table columns 


Supported Databases:
--- 
 - Oracle


Formats supported:
---
 - EXCEL
 - CSV
 - TSV

###Instalation
You can install database_loader  by cloning this Git repository
```shell script
$ python -m pip install pip install git+https://github.com/marinellirubens/database_loader#egg=database_loader
```

In order for database_loader to work you will have to install the appropriate database driver.

- Oracle: cx-Oracle version 7.0.0+

You can install this drivers via ``pip``:

    $ python3 -m pip install cx-Oracle

Usage
---
```console
$ ./csv2db -h
usage: csv2db [-h] {generate,gen,load,lo} ...

The CSV to database command line loader.
Version: 1.5.1
(c) Gerald Venzl

positional arguments:
  {generate,gen,load,lo}
    generate (gen)      Prints a CREATE TABLE SQL statement to create the
                        table and columns based on the header row of the CSV
                        file(s).
    load (lo)           Loads the data from the CSV file(s) into the database.

optional arguments:
  -h, --help            show this help message and exit
```