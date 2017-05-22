# coding=utf-8
"""
Aplicações distribuídas - Projeto 3 - queries.py
Grupo: 20
Alunos: 43551 45802 43304
"""

add={"USER":"INSERT INTO utilizadores (nome, username, password) VALUES (?,?,?)",
     "ALBUM":"INSERT INTO albuns (id_banda, nome, ano_album) VALUES(?,?,?)",
     "BANDA":"INSERT INTO bandas (nome, ano, genero) VALUES(?,?,?)",
     "RATE": "INSERT INTO listas_albuns (id_user, id_album, id_rate) VALUES(?,?,?)"
     }

show={"USER":"SELECT id,nome,username FROM utilizadores WHERE utilizadores.id=?",
      "ALBUM":"SELECT * FROM albuns WHERE albuns.id=?",
      "BANDA":"SELECT * FROM bandas WHERE bandas.id=?",
      "ALL USERS":"SELECT nome, username FROM utilizadores",
      "ALL BANDAS":"SELECT * FROM bandas",
      "ALL ALBUNS":"SELECT * FROM albuns",
      "user":"SELECT id_album,id_rate FROM listas_albuns where listas_albuns.id_user=?",
      "banda":"SELECT nome,ano_album,id_banda FROM albuns WHERE albuns.id_banda=?",
      "rate":"SELECT id_album FROM listas_albuns WHERE listas_albuns.id_rate=?"}

remove={"USER":"DELETE FROM utilizadores WHERE utilizadores.id=?",
        "ALBUM": "DELETE FROM albuns WHERE albuns.id=?",
        "BANDA": "DELETE FROM bandas WHERE bandas.id=?",
        "ALL USERS": "DELETE FROM utilizadores",
        "ALL BANDAS": "DELETE FROM bandas",
        "ALL ALBUNS": "DELETE FROM albuns",
        "user": "DELETE FROM listas_albuns where listas_albuns.id_user=?",
        "banda": "DELETE FROM albuns WHERE albuns.id_banda=?",
        "rate":"DELETE FROM listas_albuns WHERE listas_albuns.id_rate=?"}

update={"ALBUM":"UPDATE listas_albuns SET id_rate=? WHERE id_user=? AND id_album=?",
        "USER":"UPDATE utilizadores SET password=? WHERE id=?"}