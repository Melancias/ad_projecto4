# coding=utf-8
from requests_oauthlib import OAuth2Session
import os
# para nao suportar ligacao HTTPS
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# Credenciais obtidas da API github no registo da aplicação
client_id = '4a4797fe30985a8946ca'
client_secret = 'd5663c7aaeca9b1ebad183cb54045127b57186c3'
# Servidores da github para obtencao do authorization_code e do token
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
github = OAuth2Session(client_id)
# Pedido do authorization_code ao servidor de autorização (e dono do recuro a aceder)
authorization_url, state = github.authorization_url(authorization_base_url)
print 'Aceder ao link (via browser) para obter a autorizacao,', authorization_url
# Obter o authorization_code do servidor vindo no URL de redireccionamento
redirect_response = raw_input(' insira o URL devolvido no browser e cole aqui:')
# Obtencao do token
github.fetch_token(token_url, client_secret=client_secret,
authorization_response=redirect_response)
# Acesso a um recurso protegido
r = github.get('https://api.github.com/user')
print r.content