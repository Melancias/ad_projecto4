# ad_projecto4

"""
Aplicações distribuídas - Projeto 3 - README.txt
Grupo: 20
Alunos: 43551 45802 43304

Ficheiros:
    certs/cliente.crt
    certs/cliente.csr
    certs/cliente.key
    certs/root.key
    certs/root.pem
    certs/server.key
    certs/server1.crt
    certs/server1.csr
    db/__init__.py
    db/inserts.sql
    db/setup.sql
    db/work.db
    libs/database.py
    libs/queries.py
    client.py
    server.py
"""

INDEX:

0. Notes

1. Files:
  1. Main:
    1. server.py
    2. client.py
  2. Personalised libraries:
    1. __init__.py
    2. database.py
    3. queries.py
  3. Other:
    1. setup.sql
    2. inserts.sql
    3. work.db
    4. certeficados

2. iptables:
  1. Regras
  2. Testes

3. Execution examples:
  1. ADD
  2. SHOW
  3. REMOVE
  4. UPDATE

#-----------------------
0 - NOTES
#-----------------------

    O mecanismo de OAuth funciona implementado da seguinta maneira:
    Quando se abre o cliente, este redirectiona para o link de autorização fornecido pelo o servidor, no path '/login'.
    Este path redirectiona o cliente para o link de autorização do github. Este é aberto numa nova tab, no browser do cliente, e, após o login, devolve ao servidor a informação necessária, no path '/callback'.
    O callback gera uma view, que será apresentada na mesma tab préviamente gerada, com a token e uma sintese do token, para garantir a sua integridade.
    O cliente é instruido a introduzir o token apresentado, na aplicação cliente.
    Quando o cliente a introduz, este verifica a sua integridade, e incorpora a token numa cookie de sessão para garantir a autentiçidade em cada pedido.
    Qualquer pedido feito ao servidor que não tenha uma token, não pode aceder ao conteudo, recebendo uma mensagem de "Bad Authentication data." com o código 215.


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

        UNKNOW:

        When running the server for the first time, it gives the following warning:
        ```py
        127.0.0.1 - - [23/May/2017 18:22:33] "GET /login HTTP/1.1" 302 -
        /Library/Python/2.7/site-packages/requests/packages/urllib3/util/ssl_.py:334: SNIMissingWarning: An HTTPS request has been made, but the SNI (Subject Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
          SNIMissingWarning
        /Library/Python/2.7/site-packages/requests/packages/urllib3/util/ssl_.py:132: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
          InsecurePlatformWarning
        ```

        This does not affect the normal execution of the application

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

        UNKNOW:

        With every request, the client gives the following warning:
        ```py
        /Library/Python/2.7/site-packages/requests/packages/urllib3/util/ssl_.py:334: SNIMissingWarning: An HTTPS request has been made, but the SNI (Subject Name Indication) extension to TLS is not available on this platform. This may cause the server to present an incorrect TLS certificate, which can cause validation failures. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
          SNIMissingWarning
        /Library/Python/2.7/site-packages/requests/packages/urllib3/util/ssl_.py:132: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
          InsecurePlatformWarning
        /Library/Python/2.7/site-packages/requests/packages/urllib3/connection.py:340: SubjectAltNameWarning: Certificate for localhost has no `subjectAltName`, falling back to check for a `commonName` for now. This feature is being removed by major browsers and deprecated by RFC 2818. (See https://github.com/shazow/urllib3/issues/497 for details.)
          SubjectAltNameWarning
        ```

        This does not affect the normal execution of the application

2. Personalised libraries
    
    All contained in the folder libs/

    __init__.py
        
        Makes python recognize the folder libs/ as a usable library

    database.py

        Contains two functions:

        dict_factory - a static function that turns the result of a query to the sqlite database into a dictionary

        connect:db   - checks if the database exists. If it does, it connects, if it doesn't, it creates it and connects

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

    certeficados

        Contidos na pasta certs/, são os certificados usados no projeto

#-----------------------
2 - IPTABLES
#-----------------------

1. Regras

    1 - Regras base para começar:
    ```bash
    sudo /sbin/iptables -F
    sudo /sbin/iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    sudo /sbin/iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    ```

    2 - Suporte do serviço DNS (protocolos tcp e udp no porto 53)
    ```bash
    sudo /sbin/iptables -A OUTPUT -p udp --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
    sudo /sbin/iptables -A INPUT  -p udp --sport 53 -m state --state ESTABLISHED     -j ACCEPT
    sudo /sbin/iptables -A OUTPUT -p tcp --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
    sudo /sbin/iptables -A INPUT  -p tcp --sport 53 -m state --state ESTABLISHED     -j ACCEPT
    ```

    3 - Só responde a pings com origem na máquina nemo.alunos.di.fc.ul.pt:
    ```bash
    sudo /sbin/iptables -A INPUT -s nemo.alunos.di.fc.ul.pt -p icmp -j -m state --state NEW,ESTABLISHED ACCEPT
    ```

    4 - Aceita ligações de qualquer máquina no porto 5000 (porto onde o projeto corre)
    ```bash
    sudo /sbin/iptables -A INPUT -p tcp --dport 5000 -m state --state NEW,ESTABLISHED -j ACCEPT
    ```

    5 - Aceita ligações SSH da sua rede local
      10.101.148.182/23 - sub-rede local da faculdade
      10.101.0.0/24     - sub-rede da gcc
    ```bash
    sudo /sbin/iptables -A INPUT -s 10.101.148.182/23 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
    sudo /sbin/iptables -A INPUT -s 10.101.0.0/24 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
    sudo /sbin/iptables -A INPUT -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
    sudo /sbin/iptables -A OUTPUT -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
    ```

    6 - Dar permição às máquinas obrigatórias:
    ```bash
    sudo /sbin/iptables -A INPUT -d "10.101.85.6, 10.101.85.138, 10.101.85.18,10.121.53.14, 10.121.53.15, 10.101.53.16, 10.121.72.23, 10.101.148.1, 10.101.85.134" -j ACCEPT
    sudo /sbin/iptables -A OUTPUT -s "10.101.85.6, 10.101.85.138, 10.101.85.18,10.121.53.14, 10.121.53.15, 10.101.53.16, 10.121.72.23, 10.101.148.1, 10.101.85.134" -j ACCEPT
    ```

    7 - Serviço ssl:
    ```bash
    sudo /sbin/iptables -A INPUT  -p tcp -m multiport --dports 21,80,443 -m state --state NEW,ESTABLISHED -j ACCEPT
    sudo /sbin/iptables -A OUTPUT  -p tcp -m multiport --dports 21,80,443 -m state --state NEW,ESTABLISHED -j ACCEPT
    ```

    8 - Reras para acabar:
    ```bash
    sudo /sbin/iptables -A INPUT -i lo -j ACCEPT
    sudo /sbin/iptables -A OUTPUT -o lo -j ACCEPT
    sudo /sbin/iptables -A INPUT -j DROP
    sudo /sbin/iptables -A OUTPUT -j DROP
    ```

2. Testes:

    1 - o pingo proveniente de outra máquina não funciona
    ```bash
    fc43551@linux:~/Desktop/ad_projecto4$ ping -c4 10.101.148.5
    PING 10.101.148.5 (10.101.148.5) 56(84) bytes of data.

    --- 10.101.148.5 ping statistics ---
    3 packets transmitted, 0 received, 100% packet loss, time 2015ms
    ```

    Não é possivel verificar que a máquina nemo.alunos.di.fc.ul.pt.
    Contudo, conseguimos provar a cima que outra máquina da sub-rede não consegue.

    2 - Para testar que a máquina aceita ligações de qualquer outra no porto 5000, criou-se um servidor simples com a porta 5000 aberta:
      .1 - máquina com iptables
    ```bash
    fc45802@linux:~/Desktop/ad_projecto4$ python -m SimpleHTTPServer 5000
    Serving HTTP on 0.0.0.0 port 5000 ...
    10.101.148.8 - - [23/May/2017 19:03:14] "GET / HTTP/1.1" 200 -
    ^C----------------------------------------
    ```
      .2 - outra máquina:
    ```bash
    fc43551@linux:~/Desktop/ad_projecto4$ nc 10.101.148.5 5000
    GET /ad_projecto4.zip HTTP/1.1

    HTTP/1.0 404 File not found
    Server: SimpleHTTP/0.6 Python/2.7.12
    Date: Tue, 23 May 2017 18:04:41 GMT
    Connection: close
    Content-Type: text/html

    <head>
    <title>Error response</title>
    </head>
    <body>
    <h1>Error response</h1>
    <p>Error code 404.
    <p>Message: File not found.
    <p>Error code explanation: 404 = Nothing matches the given URI.
    </body>
    ```

#-----------------------
3 - EXECUTION EXAMPLES
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
