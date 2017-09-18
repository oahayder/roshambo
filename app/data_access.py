import os
import sqlite3

from flask import g


DATABASE = os.getenv('ROSHAMBO_DB')

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db

def write_to_db(query):
    cur = get_db().execute(query)
    get_db().commit()
    inserted_id = cur.lastrowid
    cur.close()

    return inserted_id

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
