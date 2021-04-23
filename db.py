import sqlite3
from datetime import datetime

import click
from flask import current_app, g
from flask.cli import with_appcontext

# learn how to use the native flask way of accessing databases
# https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def createDatabase():
    con = sqlite3.connect('logging.db')
    cur = con.cursor()

    # Create table
    cur.execute('''CREATE TABLE shower
                (date text, temperature real)''')

    # Insert a row of data
    cur.execute("INSERT INTO shower VALUES ('2021-04-20',100)")

    # Save (commit) the changes
    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()


def storeTemperature(temperature):
    con = sqlite3.connect('logging.db')
    cur = con.cursor()

    # YYYY-MM-DD HH:MM:SS.SSS
    timestamp = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S.%f")

    # Insert a row of data
    cur.execute("INSERT INTO shower VALUES (?,?)", (timestamp, temperature))

    # Save (commit) the changes
    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()

def checkDatabase():
    con = sqlite3.connect('logging.db')
    cur = con.cursor()

    # Insert a row of data
    cur.execute("select * FROM shower")
    print(cur.fetchall())

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()
