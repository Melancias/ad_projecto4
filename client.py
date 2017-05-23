# coding=utf-8
"""
Aplicações distribuídas - Projeto 3 - client.py
Grupo: 20
Alunos: 43551 45802 43304
"""
import json, requests, pprint, signal, subprocess, webbrowser, sys, hashlib



actions = ["ADD", "SHOW", "REMOVE", "UPDATE"]
genero = ["pop", "rock", "indy", "trance", "metal"]
rates = {"M": 1, "MM": 2, "S": 3, "B": 4, "MB": 5}

s = requests.session()
s.cert = ('certs/cliente.crt', 'certs/cliente.key')
s.verify = 'certs/root.pem'
session_token=None

## TODO: Se houver tempo, fazer o command HELP
## TODO: Cliente liga-> ch

def handler(signum, frame):
    print ""
    print 'closing program...'
    sys.exit()

# Control + z and Control + c handlers
signal.signal(signal.SIGTSTP, handler)
signal.signal(signal.SIGINT, handler)


def login():
    global session_token
    url = 'https://localhost:5000/login'
    if sys.platform == 'darwin':  # in case of OS X
        subprocess.Popen(['open', url])
    else:
        webbrowser.open_new_tab(url)

    tokenchecksum=raw_input("Enter here the token code given to you on the website:\n")
    token=tokenchecksum[:40]
    checksum=tokenchecksum[40:]
    if hashlib.sha256(token).hexdigest()!=checksum:
        print "Token is incorrect, restart the client and try again"
        sys.exit(-1)
    else:
        session_token=token


while True:
    try:
        if session_token==None:
            print "Login is required:"
            login()
            s.cookies.set("token",session_token)
            continue

        msg = raw_input("Comand: ").split(" ")
        data = {}
        url = 'https://localhost:5000'
        if msg[0] in actions:

            if msg[0] == "ADD":
                if msg[1] == "USER" and len(msg) == 5:
                    data = {'nome': msg[2], 'username': msg[3], 'password': msg[4]}
                    url += '/utilizadores'

                elif msg[1] == "BANDA" and len(msg) == 5:
                    if msg[4] in genero:
                        try:
                            int(msg[3])
                        except ValueError:
                            print "The year provided was not an Integer"
                            continue

                        data = {'nome': msg[2], 'ano': msg[3], 'genero': msg[4]}
                        url += '/bandas'
                    else:
                        print "Gender given is not valid\nValid genders: pop | rock | indy | metal | trance"
                        continue
                elif msg[1] == "ALBUM" and len(msg) == 5:
                    flag = False
                    try:
                        int(msg[2])
                        flag = True
                        int(msg[4])
                    except ValueError:
                        if flag:
                            print "The year provided is not an Integer"
                        else:
                            print "The ID provided was not an Integer"
                        continue
                    data = {'id_banda': msg[2], 'nome': msg[3], 'ano': msg[4]}
                    url += '/albuns'

                elif len(msg) == 4:
                    if msg[3] in rates.keys():
                        flag = False
                        try:
                            int(msg[1])
                            flag = True
                            int(msg[2])
                        except ValueError:
                            if flag:
                                print "The year provided was not an Integer"
                            else:
                                print "The ID provided was not an Integer"
                            continue
                        url += '/albuns/rate'
                        data = {'id_user': msg[1], 'id_album': msg[2], 'id_rate': rates[msg[3]]}
                    else:
                        print "Rate given is invalid\nValid Ratings: M | MM | S | B | MB"
                        continue
                else:
                    print "ADD parameters where not correct"
                    continue

                # Correu tudo bem entao faz o pedido!
                print 'url', url
                request = s.put(url=url, json=data)
                response = json.loads(request.text.encode('utf8'))
                pprint.pprint(response)

            elif msg[0] == "SHOW" or msg[0] == "REMOVE":
                if msg[1] == "USER" and len(msg) == 3:
                    try:
                        int(msg[2])
                        url += '/utilizadores/' + msg[2]
                    except ValueError:
                        print "User id provided was not an Integer"
                        continue

                elif msg[1] == "BANDA" and len(msg) == 3:
                    try:
                        int(msg[2])
                        url += '/bandas/' + msg[2]
                    except ValueError:
                        print "Band id provided was not an Integer"
                        continue

                elif msg[1] == "ALBUM" and len(msg) == 3:
                    try:
                        int(msg[2])
                        url += '/albuns/' + msg[2]
                    except ValueError:
                        print "Album id provided was not an Integer"
                        continue

                elif msg[1] == "ALL":
                    if msg[2] == "USERS" and len(msg) == 3:
                        url += '/utilizadores'

                    elif msg[2] == "BANDAS" and len(msg) == 3:
                        url += '/bandas'

                    elif msg[2] == "ALBUNS" and len(msg) == 3:
                        url += '/albuns'

                    elif msg[2] == "ALBUNS" and len(msg) == 4 and msg[3] in rates.keys():
                        url += '/albuns/rate/' + str(rates[msg[3]])

                    elif msg[2] == "ALBUNS_B" and len(msg) == 4:
                        try:
                            int(msg[3])
                            url += '/albuns/banda/' + msg[3]
                        except ValueError:
                            print "Band id provided was not an Integer"
                            continue

                    elif msg[2] == "ALBUNS_U" and len(msg) == 4:
                        try:
                            int(msg[3])
                            url += '/albuns/user/' + msg[3]
                        except ValueError:
                            print "User id provided was not an Integer"
                            continue

                    else:
                        print "REMOVE/SHOW ALL parameters where not valid"
                        continue

                else:
                    print "REMOVE/SHOW parameters where not valid"
                    continue

                # Correu tudo bem entao faz o pedido!
                if msg[0] == "SHOW":
                    print 'url', url
                    request = s.get(url=url)
                    response = json.loads(request.text.encode('utf8'))
                    pprint.pprint(response)
                else:
                    print 'url', url
                    request = s.delete(url=url)
                    response = json.loads(request.text.encode('utf8'))
                    pprint.pprint(response)

            elif msg[0] == "UPDATE":
                if msg[1] == "ALBUM" and len(msg) == 5:
                    if msg[4] in rates.keys():
                        flag = False
                        try:
                            int(msg[2])
                            flag = True
                            int(msg[3])
                        except ValueError:
                            if flag:
                                print "Album ID was not an Integer"
                            else:
                                print "User ID was not an Integer"
                            continue
                        data = {'id_user': msg[2], 'id_album': msg[3], 'id_rate': rates[msg[4]]}
                        url += '/albuns'
                    else:
                        print "Rate given is invalid\nValid Ratings: M | MM | S | B | MB"
                        continue

                elif msg[1] == "USER" and len(msg) == 4:
                    try:
                        int(msg[2])
                    except ValueError:
                        print "User ID was not an Integer"
                        continue
                    data = {'id_user': msg[2], 'password': msg[3]}
                    url += '/utilizadores'

                else:
                    print "UPDATE parameters where not valid"
                    continue

                # Correu tudo bem entao faz o pedido!
                print 'url', url
                request = s.patch(url=url, json=data)
                response = json.loads(request.text.encode('utf8'))
                pprint.pprint(response)
        else:
            print msg[0] + " is not a valid command"
            continue

    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print e.message
        print e.args
        print "ERROR"
        sys.exit()

