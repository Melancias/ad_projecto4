# coding=utf-8
"""
Aplicações distribuídas - Projeto 3 - server.py
Grupo: 20
Alunos: 43551 45802 43304
"""
import json

from flask import redirect
from flask import url_for
from requests_oauthlib import OAuth2Session

import database, queries

from flask import Flask, request,jsonify
session={}
app = Flask(__name__)
# Informação da aplicação registada no GitHub
client_id = '4a4797fe30985a8946ca'
client_secret = 'd5663c7aaeca9b1ebad183cb54045127b57186c3'
# Informação sobre a Authorization server
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

class MyException(Exception):
    """
    Class for a personalized exception.
    This way, we're able to treat certain flaws as exceptions
    """
    pass

def composeResponse(title, status, detail, url):
    """
    Builds and jsonifies the response (both error or success)
    :param title: The title of the message
    :param status: The http status code
    :param detail: The details of the message
    :param url: The url the triggered the response
    :return: a json object with the response
    """
    return jsonify({
        "title" : title,
        "status": status,
        "detail" : detail,
        "url" : url
    })

@app.errorhandler(404)
def page_not_found(e):
    """
    Handles the 404 http status occurrence
    :return: a json object composed by the function composeResponse
    """
    return composeResponse("404 Not found", 404, "Sorry m8, that url leads nowhere :/", str(request)[10:-8])

@app.route('/utilizadores', methods = ["GET","PUT","PATCH","DELETE"])
@app.route('/utilizadores/<int:id>', methods = ["GET", "DELETE"])
def utilizador(id = None):
    """
    Hanbles all requests for the base url '/utilizadores'
    :param id: the integer given in the url, None otherwise
    :return: a json object composed by the function composeResponse
    """
    res=None
    if request.method == "GET":
        # GET TODOS os users
        if id is None:
            queryAns=db.execute(queries.show['ALL USERS'])
            queryData = queryAns.fetchall()
            queryToJson=json.dumps(queryData).encode('utf8')
            res=composeResponse("All Users", 200, queryToJson, request.url_rule.rule)
        #GET 1 user
        else:
            try:
                queryAns = db.execute(queries.show['USER'],[int(id)])
                rquery = queryAns.fetchone()
                if rquery is None:
                    res=composeResponse("User not found", 204, "No User with the given id was not found in our database", request.url_rule.rule)
                else:
                    queryToJson=json.dumps(rquery).encode('utf8')
                    res=composeResponse("User id "+str(id), 200, queryToJson, request.url_rule.rule)
            except Exception as e:
                print(e.args)
                res=composeResponse("Bad request", 400, "idk wut hapen", request.url_rule.rule)
                pass

    elif request.method == "PUT":
    # Ler dados do aluno no pedido e inserir na base de dados
    # Em caso de sucesso responder com a localização do novo recurso
        try:
            data=request.json
            db.execute(queries.add['USER'],[data['nome'],data['username'],data['password']])
            conndb.commit()
            res=composeResponse("Insert successful ", 201, "User "+data['username']+" was created", request.url_rule.rule)
        except:
            res=composeResponse("Bad request", 400, "json object didn't had all the information needed", request.url_rule.rule)
            pass

    elif request.method == "DELETE":
        #delete 1
        if id is not None:
            try:
                db.execute(queries.show['USER'], [int(id)])
                if db.fetchone() is None:
                    raise MyException("User não existe")
                db.execute(queries.remove['USER'], [int(id)])
                conndb.commit()
                res=composeResponse("User deleted", 200, "The user with id "+str(id)+" was deleted", request.url_rule.rule)
            except MyException as m:
                print m.args
                res=composeResponse("User not found", 204, "No User with the given id was not found in our database", request.url_rule.rule)
                pass
            except Exception as e:
                print e.args
                res=composeResponse("Bad request", 400, "idk wut hapen", request.url_rule.rule)
                pass
        #delete todos
        else:
            db.execute(queries.remove['ALL USERS'])
            conndb.commit()
            res=composeResponse("All useres deleted", 200, "All users where deleted from the database", request.url_rule.rule)

    elif request.method == "PATCH":
        try:
            data=request.json
            db.execute(queries.show['USER'], [int(data['id_user'])])
            if db.fetchone() is None:
                raise MyException("User não existe")
            db.execute(queries.update['USER'],[data['password'],int(data['id_user'])])
            conndb.commit()
            res=composeResponse("User updated", 202, "The user with id "+str(id)+" was updated", request.url_rule.rule)
        except ValueError as ve:
            print ve.args
            res=composeResponse("ID not an Integer", 400, "Expected an Integer for the ID, but no Integer was found", request.url_rule.rule)
            pass
        except MyException as m:
            print m.args
            res=composeResponse("User not found", 204, "No User with the given id was not found in our database", request.url_rule.rule)
            pass
        except Exception as e:
            print e.args
            res=composeResponse("Bad request", 400, "idk wut hapen", request.url_rule.rule)
            pass

    return res

@app.route('/bandas', methods = ["GET","PUT","DELETE"])
@app.route('/bandas/<int:id>', methods = ["GET", "DELETE"])
def bandas(id = None):
    """
    Hanbles all requests for the base url '/bandas'
    :param id: the integer given in the url, None otherwise
    :return: a json object composed by the function composeResponse
    """
    res = None
    if request.method == "GET":
        # GET Todas as bandas
        if id is None:
            c = db.execute(queries.show['ALL BANDAS'])
            rquery = c.fetchall()
            queryToJson=json.dumps(rquery).encode('utf8')
            res=composeResponse("Every band", 200, queryToJson, request.url_rule.rule)
        # GET 1 banda
        else:
            try:
                c = db.execute(queries.show['BANDA'], [int(id)])
                rquery = c.fetchone()
                if rquery is None:
                    res=composeResponse("Band not found", 204, "No Band with the given id was not found in our database", request.url_rule.rule)
                else:
                    queryToJson=json.dumps(rquery).encode('utf8')
                    res=composeResponse("Band id "+str(id), 200, queryToJson, request.url_rule.rule)
            except:
                res=composeResponse("Bad request", 400, "idk wut hapen", request.url_rule.rule)
                pass

    elif request.method == "PUT":
        # Ler dados do aluno no pedido e inserir na base de dados
        # Em caso de sucesso responder com a localização do novo recurso
        try:
            data = request.json
            db.execute(queries.add['BANDA'], [data['nome'], int(data['ano']), data['genero']])
            conndb.commit()
            res=composeResponse("Insert successful ", 201, "Band "+data['nome']+" was created", request.url_rule.rule)
        except ValueError as ve:
            print ve.args
            res=composeResponse("Ano not an Integer", 400, "Expected an Integer for 'ano' (year), but no Integer was found", request.url_rule.rule)
            pass
        except:
            print "Pedido JSON provavelmente vazio"
            res=composeResponse("Bad request", 400, "json object didn't had all the information needed", request.url_rule.rule)
            pass

    elif request.method == "DELETE":
        if id is not None:
            try:
                db.execute(queries.show['BANDA'], [int(id)])
                if db.fetchone() is None:
                    raise MyException("Banda não existe")
                db.execute(queries.remove['BANDA'], [int(id)])
                conndb.commit()
                res=composeResponse("Band deleted", 200, "Band "+str(id)+" was deleted", request.url_rule.rule)
            except MyException as m:
                print m.args
                res=composeResponse("Band not found", 204, "No Band with the given id was not found in our database", request.url_rule.rule)
                pass
            except Exception as e:
                print e.args
                res=composeResponse("Bad request", 400, "idk wut hapen", request.url_rule.rule)
                pass
        #delete todos
        else:
            db.execute(queries.remove['ALL BANDAS'])
            conndb.commit()
            res=composeResponse("All bands deleted", 200, "All users where deleted from the database", request.url_rule.rule)

    return res

@app.route('/albuns', methods = ["GET","PUT","DELETE", "PATCH"])
@app.route('/albuns/<int:id>', methods = ["GET","DELETE"])
@app.route('/albuns/banda/<int:id>', methods = ["GET","DELETE"])
@app.route('/albuns/user/<int:id>', methods = ["GET","DELETE"])
@app.route('/albuns/rate', methods = ["PUT"])
@app.route('/albuns/rate/<int:id>', methods = ["GET","DELETE"])
def albuns(id = None):
    """
    Hanbles all requests for the base url '/albuns'
    :param id: the integer given in the url, None otherwise
    :return: a json object composed by the function composeResponse
    """
    res=None
    action=None
    actionlist=request.url_rule.rule.split("/")
    if len(actionlist)>3 or (len(actionlist)==3 and actionlist[2] == 'rate'):
        action=actionlist[2]
    if request.method == "GET":
        # GET TODOS os users
        if id is None:
            c=db.execute(queries.show['ALL ALBUNS'])
            rquery = c.fetchall()
            queryToJson=json.dumps(rquery).encode('utf8')
            res=composeResponse("All albums", 200, queryToJson, request.url_rule.rule)
        #GET 1 user
        else:
            print action
            if action is None:
                c = db.execute(queries.show['ALBUM'],[int(id)])
                rquery = c.fetchone()
                if rquery is None:
                    res=composeResponse("Album not found", 204, "No Album with the given id was not found in our database", request.url_rule.rule)
                else:
                    queryToJson=json.dumps(rquery).encode('utf8')
                    res=composeResponse("Album id "+str(id), 200, queryToJson, request.url_rule.rule)
            elif action in ['user','rate','banda']:
                c = db.execute(queries.show[action], [int(id)])
                rquery = c.fetchall()
                if len(rquery)<1:
                    res=composeResponse("No such association", 204, "No Album with an association to " + str(id) + " was not found in our database", request.url_rule.rule)
                else:
                    queryToJson=json.dumps(rquery).encode('utf8')
                    res=composeResponse("All albums related to "+str(id), 200, queryToJson, request.url_rule.rule)

            else:
                res=composeResponse("Bad request", 400, "Invalid option for albums (needs to be: 'user' or 'rate' or 'banda'", request.url_rule.rule)
                pass

    if request.method == "PUT":
    # Ler dados do aluno no pedido e inserir na base de dados
    # Em caso de sucesso responder com a localização do novo recurso
        if action is None:
            flag = False
            try:
                data=request.json
                #no lado do cliente converter a letra no codigo B 4 MB 5
                id_banda = int(data['id_banda'])
                flag = True
                ano = int(data['ano'])
                db.execute(queries.add['ALBUM'],[id_banda, data['nome'], ano])
                conndb.commit()
                res=composeResponse("Insert successful ", 201, "Album "+data['nome']+" was created", request.url_rule.rule)
            except ValueError as ve:
                print ve.args
                if flag:
                    res=composeResponse("ID not an Integer", 400, "Expected an Integer for 'ano' (year), but no Integer was found", request.url_rule.rule)
                else:
                    res=composeResponse("ID not an Integer", 400, "Expected an Integer for the ID, but no Integer was found", request.url_rule.rule)
                pass
            except:
                print "Pedido JSON provavelmente vazio"
                res=composeResponse("Bad request", 400, "idk wut hapen", request.url_rule.rule)
                pass
        else:
            flag = 'u'
            try:
                data = request.json
                user = int(data['id_user'])
                flag = 'a'
                album = int(data['id_album'])
                flag = 'r'
                rate = int(data['id_rate'])
                db.execute(queries.add['RATE'], [user, album, rate])
                conndb.commit()
                res=composeResponse("Rated", 201, "User "+str(user)+" rated the album "+str(album), request.url_rule.rule)
            except ValueError as ve:
                print ve.args
                if flag == 'u':
                    res=composeResponse("ID not an Integer", 400, "Expected an Integer for the user ID, but no Integer was found", request.url_rule.rule)
                elif flag == 'a':
                    res=composeResponse("ID not an Integer", 400, "Expected an Integer for the album ID, but no Integer was found", request.url_rule.rule)
                else:
                    res=composeResponse("ID not an Integer", 400, "Expected an Integer for the rate ID, but no Integer was found", request.url_rule.rule)
                pass
            except Exception as e:
                print e.args
                print "Pedido JSON provavelmente vazio"
                res=composeResponse("Bad request", 400, "json object didn't had all the information needed", request.url_rule.rule)
                pass

    if request.method == "DELETE":
        if id is not None:
            if action is None:
                try:
                    db.execute(queries.show['ALBUM'], [int(id)])
                    if db.fetchone() is None:
                        raise MyException("album não existe")
                    db.execute(queries.remove['ALBUM'], [int(id)])
                    conndb.commit()
                    res=composeResponse("Album deleted", 200, "Album "+str(id)+" was deleted", request.url_rule.rule)
                except MyException as m:
                    print m.args
                    res=composeResponse("Album not found", 204, "No Album with the given id was not found in our database", request.url_rule.rule)
                    pass
                except Exception as e:
                    print e.args
                    res=composeResponse("Bad request", 400, "idk wut hapen", request.url_rule.rule)
                    pass
            elif action in ['user','rate','banda']:
                try:
                    db.execute(queries.show[action], [int(id)])
                    if db.fetchone() is None:
                        raise MyException("album não existe")
                    db.execute(queries.remove[action], [int(id)])
                    conndb.commit()
                    res=composeResponse("Albums deleted", 200, "All albums related to "+str(id)+" deleted", request.url_rule.rule)
                except MyException as m:
                    print m.args
                    res=composeResponse("Album not found", 204, "No Album with the given id was not found in our database", request.url_rule.rule)
                    pass
                except Exception as e:
                    print e.args
                    res=composeResponse("Bad request", 400, "idk wut hapen", request.url_rule.rule)
                    pass
            else:
                res=composeResponse("Bad request", 400, "Invalid option for albums (needs to be: 'user' or 'rate' or 'banda'", request.url_rule.rule)
                pass
        #delete todos
        else:
            db.execute(queries.remove['ALL ALBUNS'])
            conndb.commit()
            res=composeResponse("All album deleted", 200, "All album where deleted", request.url_rule.rule)

    if request.method == "PATCH":
        flag = False
        try:
            data=request.json
            album = int(data['id_album'])
            db.execute(queries.show['ALBUM'], [album])
            if db.fetchone() is None:
                raise MyException("Album não existe")
            flag = True
            user = int(data['id_user'])
            rate = int(data['id_rate'])
            db.execute(queries.update['ALBUM'], [rate, user, album])
            conndb.commit()
            res=composeResponse("Album updated", 202, "The rating of the album with id "+str(album)+" was updated by the user with id "+str(user), request.url_rule.rule)
        except ValueError as ve:
            print ve.args
            if flag:
                res=composeResponse("ID not an Integer", 400, "Expected an Integer for the user ID, but no Integer was found", request.url_rule.rule)
            else:
                res=composeResponse("ID not an Integer", 400, "Expected an Integer for the album ID, but no Integer was found", request.url_rule.rule)
            pass
        except MyException as m:
            print m.args
            res=composeResponse("Album not found", 204, "No Album with the given id was not found in our database", request.url_rule.rule)
            pass
        except Exception as e:
            print e.args
            res=composeResponse("Bad request", 400, "idk wut hapen", request.url_rule.rule)
            pass

    return res

@app.route("/login")
def login():
 github = OAuth2Session(client_id)
 authorization_url, state = github.authorization_url(authorization_base_url)
 # State is used to prevent CSRF, keep this for later.
 session['oauth_state'] = state
 return redirect(authorization_url)

@app.route("/callback", methods=["GET"])
def callback():
     github = OAuth2Session(client_id, state=session['oauth_state'])
     token = github.fetch_token(token_url,
     client_secret=client_secret,
     authorization_response=request.url)
     session['oauth_token'] = token
     return redirect(url_for('.profile'))

@app.route("/profile", methods=["GET"])
def profile():
    github = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(github.get('https://api.github.com/user').json())



if __name__ == '__main__':
    context = ('certs/server1.crt', 'certs/server.key')
    conndb, db = database.connect_db('work.db')
    app.run(debug = True,threaded=True,ssl_context=context)