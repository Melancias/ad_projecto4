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
    work.db
"""

INDEX:

1. Files:
  1. Main:
    1. server.py
    2. client.py
  2. Personalised libraries:
    1. database.py
    2. queries.py
  3. Other:
    1. setup.sql
    2. inserts.sql
    3. work.db
2. Execution examples:
  1. ADD
  2. SHOW
  3. REMOVE
  4. UPDATE

#-----------------------
1 - FILES
#-----------------------

1. Main

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
            ADD BANDA <nome> <ano> <genero> *problema com a identação (ver exemplos de comando)
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

2. Personalised libraries

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

3. Other:

    setup.sql

        An sql file with the instructions to create the tables asked and populate the rates table

    inserts.sql

        An sql file with some INSERT queries to populate the database

    work.db

        The db for the server

#-----------------------
2 - EXECUTION EXAMPLES
#-----------------------

-----------------------
1. ADD
  de um USER:
    comando: ADD USER grupo20 G20 pass20

    resposta: {u'detail': u'User G20 was created',
               u'status': 201,
               u'title': u'Insert successful ',
               u'url': u'/utilizadores'}

  de uma BANDA:
    comando: ADD BANDA banda20 ano rock

    resposta: The year provided was not an Integer

    comando: ADD BANDA banda20 2017 classico

    resposta:Gender given is not valid
             Valid genders: pop | rock | indy | metal | trance

    comando: ADD BANDA banda20 2017 trance

    resposta: {u'detail': u'Band banda20 was created',
               u'status': 201,
               u'title': u'Insert successful ',
               u'url': u'/bandas'}

  de um ALBUM:
    comando: ADD ALBUM a album20 2017

    resposta: The ID provided was not an Integer

    comando: ADD ALBUM 1 album20 ano

    resposta: The year provided is not an Integer

    comando: ADD ALBUM 1 album20 2017

    resposta: {u'detail': u'Album album20 was created',
               u'status': 201,
               u'title': u'Insert successful ',
               u'url': u'/albuns'}

  de uma RATE:
    comando: ADD a 1 MB

    resposta: The ID provided was not an Integer

    comando: ADD 1 a MB

    resposta: The year provided was not an Integer (should say id, but ups. Either way, verification is being done)

    comando: ADD 1 1 a

    resposta: Rate given is invalid
              Valid Ratings: M | MM | S | B | MB

    comando: ADD 1 1 MB

    resposta: {u'detail': u'User 1 rated the album 1',
               u'status': 201,
               u'title': u'Rated',
               u'url': u'/albuns/rate'}

-----------------------
2. SHOW
  comando: SHOW USER a

  resposta: User id provided was not an Integer

  comando: SHOW USER 7

  resposta: {u'detail': u'No User with the given id was not found in our database',
             u'status': 204,
             u'title': u'User not found',
             u'url': u'/utilizadores/<int:id>'}

  comando: SHOW USER 1

  resposta: {u'detail': u'{"username": "G20", "id": 1, "nome": "grupo20"}',
             u'status': 200,
             u'title': u'User id 1',
             u'url': u'/utilizadores/<int:id>'}

  comando: SHOW BANDA a

  resposta: Band id provided was not an Integer

  comando: SHOW BANDA 7

  resposta: {u'detail': u'No Band with the given id was not found in our database',
             u'status': 204,
             u'title': u'Band not found',
             u'url': u'/bandas/<int:id>'}

  comando: SHOW BANDA 1

  resposta: {u'detail': u'{"ano": 2017, "genero": "trance", "id": 1, "nome": "banda20"}',
             u'status': 200,
             u'title': u'Band id 1',
             u'url': u'/bandas/<int:id>'}

  comando: SHOW ALBUM a

  response: Album id provided was not an Integer

  comando: SHOW ALBUM 7

  response: {u'detail': u'No Album with the given id was not found in our database',
             u'status': 204,
             u'title': u'Album not found',
             u'url': u'/albuns/<int:id>'}

  comando: SHOW ALBUM 1

  response: {u'detail': u'{"id_banda": 1, "id": 1, "ano_album": 2017, "nome": "album20"}',
             u'status': 200,
             u'title': u'Album id 1',
             u'url': u'/albuns/<int:id>'}

  comando: SHOW ALL USERS

  resposta: {u'detail': u'[{"username": "G20", "nome": "grupo20"},
                           {"username": "CENAS", "nome": "CENAS"},
                           {"username": "CENAS", "nome": "CENAS"},
                           {"username": "CENAS", "nome": "CENAS"}]',
             u'status': 200,
             u'title': u'All Users',
             u'url': u'/utilizadores'}

  comando: SHOW ALL BANDAS

  resposta: {u'detail': u'[{"ano": 2017, "genero": "trance", "id": 1, "nome": "banda20"},
                           {"ano": 2017, "genero": "trance", "id": 2, "nome": "banda20"}]',
             u'status': 200,
             u'title': u'Every band',
             u'url': u'/bandas'}

  comando: SHOW ALL ALBUNS

  resposta: {u'detail': u'[{"id_banda": 1, "id": 1, "ano_album": 2017, "nome": "album20"},
                           {"id_banda": 2, "id": 2, "ano_album": 2010, "nome": "wupwup"}]',
             u'status': 200,
             u'title': u'All albums',
             u'url': u'/albuns'}

  comando: SHOW ALL ALBUNS_B a

  resposta: Band id provided was not an Integer

  comando: SHOW ALL ALBUNS_B 1

  resposta: {u'detail': u'[{"id_banda": 1, "ano_album": 2017, "nome": "album20"}]',
             u'status': 200,
             u'title': u'All albums related to 1',
             u'url': u'/albuns/banda/<int:id>'}

  comando: SHOW ALL ALBUNS_U a

  resposta: User id provided was not an Integer

  comando: SHOW ALL ALBUNS_U 1

  resposta: {u'detail': u'[{"id_rate": 5, "id_album": 1}]',
             u'status': 200,
             u'title': u'All albums related to 1',
             u'url': u'/albuns/user/<int:id>'}

  comando: SHOW ALL ALBUNS a

  resposta: REMOVE/SHOW ALL parameters where not valid

  comando: SHOW ALL ALBUNS MB

  resposta: {u'detail': u'[{"id_album": 1}]',
             u'status': 200,
             u'title': u'All albums related to 5',
             u'url': u'/albuns/rate/<int:id>'}

  comando: SHOW a

  resposta: REMOVE/SHOW ALL parameters where not valid

  comando: SHOW ALL a

  resposta: REMOVE/SHOW parameters where not valid


-----------------------
3. REMOVE
  comando: REMOVE USER a

  resposta: User id provided was not an Integer

  comando: REMOVE USER 7

  resposta: {u'detail': u'No User with the given id was not found in our database',
             u'status': 204,
             u'title': u'User not found',
             u'url': u'/utilizadores/<int:id>'}

  comando: REMOVE USER 1

  resposta: {u'detail': u'The user with id 2 was deleted',
             u'status': 200,
             u'title': u'User deleted',
             u'url': u'/utilizadores/<int:id>'}

  comando: REMOVE BANDA a

  resposta: Band id provided was not an Integer

  comando: REMOVE BANDA 7

  resposta: {u'detail': u'No Band with the given id was not found in our database',
             u'status': 204,
             u'title': u'Band not found',
             u'url': u'/bandas/<int:id>'}

  comando: REMOVE BANDA 1

  resposta: {u'detail': u'Band 1 was deleted',
             u'status': 200,
             u'title': u'Band deleted',
             u'url': u'/bandas/<int:id>'}

  comando: REMOVE ALBUM a

  response: Album id provided was not an Integer

  comando: REMOVE ALBUM 7

  response: {u'detail': u'No Album with the given id was not found in our database',
             u'status': 204,
             u'title': u'Album not found',
             u'url': u'/albuns/<int:id>'}

  comando: REMOVE ALBUM 1

  response: {u'detail': u'Album 1 was deleted',
             u'status': 200,
             u'title': u'Album deleted',
             u'url': u'/albuns/<int:id>'}

  comando: REMOVE ALL USERS

  resposta: {u'detail': u'All users where deleted from the database',
             u'status': 200,
             u'title': u'All useres deleted',
             u'url': u'/utilizadores'}

  comando: REMOVE ALL BANDAS

  resposta: {u'detail': u'All users where deleted from the database',
             u'status': 200,
             u'title': u'All bands deleted',
             u'url': u'/bandas'}

  comando: REMOVE ALL ALBUNS

  resposta: {u'detail': u'All album where deleted',
             u'status': 200,
             u'title': u'All album deleted',
             u'url': u'/albuns'}

  comando: REMOVE ALL ALBUNS_B a

  resposta: Band id provided was not an Integer

  comando: REMOVE ALL ALBUNS_B 7

  resposta: {u'detail': u'No Album with the given id was not found in our database',
             u'status': 204,
             u'title': u'Album not found',
             u'url': u'/albuns/banda/<int:id>'}

  comando: REMOVE ALL ALBUNS_B 1

  resposta: {u'detail': u'All albums related to 1 deleted',
             u'status': 200,
             u'title': u'Albums deleted',
             u'url': u'/albuns/banda/<int:id>'}

  comando: REMOVE ALL ALBUNS_U a

  resposta: User id provided was not an Integer

  comando: REMOVE ALL ALBUNS_U 7

  resposta: {u'detail': u'No Album with the given id was not found in our database',
             u'status': 204,
             u'title': u'Album not found',
             u'url': u'/albuns/user/<int:id>'}

  comando: REMOVE ALL ALBUNS_U 1

  resposta: {u'detail': u'All albums related to 1 deleted',
             u'status': 200,
             u'title': u'Albums deleted',
             u'url': u'/albuns/user/<int:id>'}

  comando: REMOVE ALL ALBUNS a

  resposta: REMOVE/SHOW ALL parameters where not valid

  comando: REMOVE ALL ALBUNS MB

  resposta: {u'detail': u'All albums related to 5 deleted',
             u'status': 200,
             u'title': u'Albums deleted',
             u'url': u'/albuns/rate/<int:id>'}

-----------------------
4. UPDATE
  comando: UPDATE ALBUM 1 7 MB

  resposta: {u'detail': u'No Album with the given id was not found in our database',
             u'status': 204,
             u'title': u'Album not found',
             u'url': u'/albuns'}

  comando: UPDATE ALBUM a 1 MB

  resposta: User ID was not an Integer

  comando: UPDATE ALBUM 1 1 MB

  resposta: {u'detail': u'The rating of the album with id 1 was updated by the user with id 1',
             u'status': 202,
             u'title': u'Album updated',
             u'url': u'/albuns'}

  comando: UPDATE USER a a

  resposta: User ID was not an Integer

  comando: UPDATE USER 7 a

  resposta: {u'detail': u'No User with the given id was not found in our database',
             u'status': 204,
             u'title': u'User not found',
             u'url': u'/utilizadores'}

  comando: UPDATE USER 1 a

  resposta: {u'detail': u'The user with id None was updated',
             u'status': 202,
             u'title': u'User updated',
             u'url': u'/utilizadores'}
