from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User

class Bug:
    def __init__(self, data):
        self.id                 = data['id']
        self.title              = data['title']
        self.description        = data['description']
        self.user_id            = data['user_id']
        self.created_at         = data['created_at']
        self.updates            = []
        self.developers         = []


    # Validate Bug
    @staticmethod
    def validate_bug(bug, methods=['POST']):
        is_valid = True # we assume this is true
        if len(bug['title']) < 5:
            flash("Title must be at least 5 characters.")
            is_valid = False
        if len(bug['description']) < 5:
            flash("Description must be at least 5 characters.")
            is_valid = False
        return is_valid


    # Add/Save a Bug
    @classmethod
    def add_bug(cls, data):
        query = "INSERT INTO bugs (title, description, user_id, created_at) VALUES ( %(title)s, %(description)s, %(user_id)s, NOW() ) "
        return connectToMySQL().query_db(query, data)


    # Get All Bugs
    @classmethod
    def get_all_bugs(cls):
        query = "SELECT * FROM bugs "
        return connectToMySQL().query_db(query)


    # Get All Bugs with Last Update
    # See: https://www.sisense.com/blog/4-ways-to-join-only-the-first-row-in-sql/
    @classmethod
    def get_all_bugs_with_last_update(cls):
        query = "SELECT * FROM bugs JOIN(SELECT id, description as update_description, created_at as update_created_at, bug_id, user_id FROM updates WHERE id in (SELECT max(id) FROM updates GROUP BY bug_id)) AS most_recent_update ON bugs.id = most_recent_update.bug_id JOIN(SELECT id, first_name as bug_user_first_name, last_name as bug_user_last_name FROM users) AS bug_user ON bug_user.id = bugs.user_id JOIN(SELECT id, first_name as update_user_first_name, last_name as update_user_last_name FROM users) AS update_user ON update_user.id = bugs.user_id "
        return connectToMySQL().query_db(query)


    # Get Bug By ID
    @classmethod
    def get_bug_by_id(cls, data):
        query = "SELECT * FROM bugs WHERE id = %(id)s"
        return connectToMySQL().query_db(query, data)[0]

    # Get Bug By ID with User Data
    @classmethod
    def get_bug_by_id_with_user_data(cls, data):
        query = "SELECT * FROM bugs LEFT JOIN users ON users.id = bugs.user_id WHERE bugs.id = %(id)s"
        return connectToMySQL().query_db(query, data)[0]

    