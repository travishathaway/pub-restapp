import sqlite3
from flask.ext.restful import Resource, abort, fields, marshal_with
from .arguments import create_user_parser, update_user_parser
from .app import get_db
from .database import create_user, update_user


class BaseResource(Resource):
    def __init__(self, *args, **kwargs):
        self.db = get_db()
        self.cursor = self.db.cursor()
        super(BaseResource, self).__init__(*args, **kwargs)


class Index(BaseResource):
    def get(self):
        """
        The index of your restapi
        """
        return {
            'message': 'Welcome to restapp. The sample Flask Restful'
                       ' tutorial app'
        }


class User(BaseResource):
    def get(self, user_id):
        """
        This is the user resource. Given a user ID, this will
        return information about the user.
        """
        res = self.cursor.execute('SELECT * FROM users WHERE id = ?', user_id)
        row = res.fetchone()
        self.cursor.close()

        if row:
            return {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'favorite_color': row[3],
            }
        else:
            return abort(404, message='User not found')

    def put(self, user_id):
        """
        Update the user

        :param user_id: Integer
        """
        args = update_user_parser.parse_args()
        res = self.cursor.execute("SELECT id FROM users WHERE id = ?", user_id)
        row = res.fetchone()

        if row:
            update_user(user_id, args)

            return self.get(user_id)

        else:
            # User not found
            return abort(404, message='User not found')

    def delete(self, user_id):
        """
        Remove the user

        :param user_id: Integer
        """
        self.cursor.execute("DELETE FROM users WHERE id = ?", user_id)

        return {
            'message': 'User deleted'
        }


class UserList(BaseResource):
    def get(self):
        """
        This is the user resource. Given a user ID, this will
        return information about the user.
        """
        res = self.cursor.execute(
            "SELECT id, username, email, favorite_color FROM users"
        )
        rows = res.fetchall()
        self.cursor.close()

        results = [
            {'id': row[0],
             'username': row[1],
             'email': row[2],
             'favorite_color': row[3]}
            for row in rows
        ]

        return results or []

    def post(self):
        """
        Create a new user
        """
        args = create_user_parser.parse_args()
        return create_user(args)
