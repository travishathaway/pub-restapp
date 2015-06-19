import sqlite3
from .app import app, get_db


def init_db():
    """
    Initialize our database by creating a couple tables
    """
    with app.app_context():
        db = get_db().cursor()
        res = db.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='users'
            """)

        if not res.fetchall():
            db.execute(
                """
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    email TEXT,
                    favorite_color TEXT
                )""")


def create_user(data):
    """
    Puts a user in our database
    :param data:
    :return: Dictionary
    """
    cursor = get_db().cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, favorite_color) VALUES (?, ?, ?)",
            [data.get('username'), data.get('email'), data.get('favorite_color')]
        )
    except sqlite3.IntegrityError:
        return {
                   'message': 'User with provided username already exists'
               }, 400

    res = cursor.execute(
        "SELECT id, username, email, favorite_color FROM users WHERE username = ?",
        [data.get('username'), ]
    )
    row = res.fetchone()
    cursor.close()

    return {
        'id': row[0],
        'username': row[1],
        'email': row[2],
        'favorite_color': row[3]
    }


def update_user(user_id, data):
    """
    Updates a user in our database
    :param data:
    :return: Dictionary
    """
    cursor = get_db().cursor()

    updates = []
    params = []

    if data.get('email'):
        updates.append("email = ?")
        params.append(data.get('email'))
    if data.get('favorite_color'):
        updates.append("favorite_color = ?")
        params.append(data.get('favorite_color'))
    if updates:
        params.append(user_id)
        update_str = ', '.join(updates)
        sql_string = 'UPDATE users SET {} WHERE id = ?'.format(update_str)
        cursor.execute(sql_string, params)
