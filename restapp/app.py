from flask import Flask, g
from flask.ext import restful
import sqlite3


# Create your flask app object
app = Flask(__name__)
# Import your config variables
app.config.from_pyfile('config.py')
# Create your restapi object
api = restful.Api(app)

# Code for the database
def get_db():
    """
    Returns our db cursor
    :return: cursor
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DB_LOCATION'])
    return db

# This ensures we always commit our transaction and close the db connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.commit()
        db.close()

from .restapi import (
    Index, UserList, User
)

# Register all the routes in your REST API
api.add_resource(Index, '/')
api.add_resource(User, '/user/<user_id>', endpoint='user')
api.add_resource(UserList, '/user', endpoint='userlist')
