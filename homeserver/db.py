import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

# https://flask.palletsprojects.com/en/1.1.x/tutorial/database/

# opens up and connects to a database if it's not already open
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# close the database if it's open
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# open database and run the schema.sql script 
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# drop and recreate database with "flask init-db" in cli
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# create database instance 
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

