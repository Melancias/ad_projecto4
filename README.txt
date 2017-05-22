"""
Aplicações distribuídas - Projeto 3 - README.txt
Grupo: 20
Alunos: 43551 45802 43304

Ficheiros:
    database.py
    server.py
    queries.py
    client.py
    setup.sql
    inserts.sql
    README.txt
"""

INDEX:

1. Main programs:
    1. server.py
    2. client.py
2. Personalised libraries:
    1. database.py
    2. queries.py
3. Other:
    1. setup.sql
    2. inserts.sql

Main programs

    server.py:

        Imports `json` and the two personalised libraries, `database` `queries` (detailed later)

        How to run:
        ```bash
        $ python server.py
        ```

        When initialized, the server will use the library `database.py` to connect to the database file. If said file doesn't exist, it will create one.
        Every response from the server (be it either a success or an error) is a json object that follows the following format:
        {
            "title" : title,
            "status": status,
            "detail" : detail,
            "url" : url
        }
        where:
            · title ("title")       -> the title of the message. Tells what the message is about in a simple statement
            · status ("httpStatus") -> the http status code. This can be one of the following:
                [ 200 (if the operation was successful and not an insert or update),
                  201 (if an insert was successful), 202 (if an update was successful),
                  204 (if what was asked wasn't in the database), 400 (in case of a bad request),
                  404 (in the case someone is trying to access an url that doesn't exist) ]
            · detail ("detail")     -> the result from the operation. (it can be either the object resulting from the operation or a statement detailing the error)
            · url ("describedBy")   -> the url requested

        The server is capable of handling a 404 error.
        The server as a class MyException(Exception). This Exception is raises in specific occasions so it's easier to treat.
        The queries used by the server are stored in the library `queries`.

    client.py:

        Imports `json`, `request`, `pprint`, `sys` and `signal`

        How to run:
        ```bash
        $ python client.py
        ```

        Available commands:
            #### ----------------------
            ## ------- ADD ----------

            ADD USER <nome> <username> <password>
            ADD BANDA <nome> <ano> <genero>
            ADD ALBUM <id_banda> <nome> <ano album>
            ADD <id_user> <id_album> <rate>

            #### ----------------------
            ## ------- REMOVE -------

            REMOVE USER <id_user>
            REMOVE BANDA <id_banda>
            REMOVE ALBUM <id_album>
            REMOVE ALL <USERS | BANDAS | ALBUNS>
            REMOVE ALL ALBUNS_B <id_banda>
            REMOVE ALL ALBUNS_U <id_user>
            REMOVE ALL ALBUNS <rate>

            #### ----------------------
            ## ------- SHOW ---------

            SHOW USER <id_user>
            SHOW BANDA <id_banda>
            SHOW ALBUM <id_album>
            SHOW ALL <USERS | BANDAS | ALBUNS>
            SHOW ALL ALBUNS_B <id_banda>
            SHOW ALL ALBUNS_U <id_user>
            SHOW ALL ALBUNS <rate>

            #### ----------------------
            ## ------- UPDATE -------

            UPDATE ALBUM <id_user> <id_album> <rate>
            UPDATE USER <id_user> <password>

        The client verifies when an input that should be an Integer is or isn't so, if the command is valid, if the gender is valid and if the rate is valid
        The program cam be safely shut down, by pressing either ctrl+C or ctrl+Z
        In the eventuality of an unexpected error occurring, if will print 'ERROR' and exit the program

Personalised libraries

    database.py

        Contains two functions:

        dict_factory - a static function that turns the result of a query to the sqlite database into a dictionary

        connect:db   - checks if the database exists. If it does, it connects, if it doesn't, it creats it and connects

    queries.py

        Contains 4 dictionaries with all the necessary queries:

        'add'    - contains every INSERT query
        'show'   - contains every SELECT query
        'remove' - contains every DELETE query
        'update' - contains every UPDATE query

Other:

    setup.sql

        An sql file with the instructions to create the tables asked and populate the rates table

    inserts.sql

        An sql file with some INSERT queries to populate the database
