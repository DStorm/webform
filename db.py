import sqlite3

import click
from flask import current_app, g
from flask.blueprints import Blueprint
from flask.cli import with_appcontext

init = Blueprint('init-db', __name__)

def get_db():
    # check if g has a connection
    if 'db' not in g:
        # get a new connection
        g.db = sqlite3.connect(
            "webform.db",
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # set row factory, that each row of a query is represented as a dict
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    # get and remove the 'db' object from g
    # assign the reference to variable db
    # if g has property db, variable db will be none
    db = g.pop('db', None)

    # if db has a reference to a connection object
    # connection needs to be closed 
    if db is not None:
        db.close()

def init_db():
    # get a connection to the database
    db = get_db()

    # open the schema sql to build the database tables
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# decorator to link the cli command 'init db' to the function below
@init.cli.command('init')
# decorator to use tha pp context
@with_appcontext
def init_db_command():
    # init the database from the schema.sql file
    init_db()
    # echo to the command line
    click.echo('Database initialised!')


def init_app(app):
    # before initialising the app, close exisitng resources
    # here make sure no database connection is already running
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)