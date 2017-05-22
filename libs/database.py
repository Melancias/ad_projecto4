# coding=utf-8
"""
Aplicações distribuídas - Projeto 3 - database.py
Grupo: 20
Alunos: 43551 45802 43304
"""
import sqlite3
from os.path import isfile

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_db(dbname):
    # Existe ficheiro da base de dados?
    db_is_created = isfile(dbname)

    connection = sqlite3.connect(dbname, check_same_thread=False)
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    if not db_is_created:
        cursor.executescript(open("db/setup.sql").read())
        connection.commit()
    return connection, cursor