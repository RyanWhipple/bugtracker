from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

class Update:
    def __init__(self, data):
        self.id                 = data['id']
        self.description        = data['description']
        self.user_id            = data['user_id']
        self.bug_id             = data['bug_id']
        self.created_at         = data['created_at']


    # Validate Update
    @staticmethod
    def validate_update(update, methods=['POST']):
        is_valid = True # we assume this is true
        if len(update['description']) < 5:
            flash("Description must be at least 5 characters.")
            is_valid = False
        return is_valid


    # Add/Save a Update
    @classmethod
    def add_update(cls, data):
        query = "INSERT INTO updates (description, user_id, bug_id, created_at) VALUES ( %(description)s, %(user_id)s, %(bug_id)s, NOW() ) "
        return connectToMySQL().query_db(query, data)


    # Get All Updates
    @classmethod
    def get_all_updates(cls):
        query = "SELECT * FROM updates "
        return connectToMySQL().query_db(query)


    # Get Update By ID
    @classmethod
    def get_update_by_id(cls, data):
        query = "SELECT * FROM updates WHERE id = %(id)s"
        return connectToMySQL().query_db(query, data)[0]


    # Get Update By ID with User Data
    @classmethod
    def get_update_by_id_with_user_data(cls, data):
        query = "SELECT * FROM updates LEFT JOIN users ON users.id = updates.user_id WHERE updates.id = %(id)s"
        return connectToMySQL().query_db(query, data)


    # Get Updates By "bug_id"
    @classmethod
    def get_updates_by_bug_id(cls, data):
        query = "SELECT * FROM updates WHERE bug_id = %(id)s"
        return connectToMySQL().query_db(query, data)


    # Get Updates By "bug_id" with User Data
    @classmethod
    def get_updates_by_bug_id_with_user_data(cls, data):
        query = "SELECT * FROM updates LEFT JOIN users ON users.id = updates.user_id WHERE bug_id = %(id)s"
        return connectToMySQL().query_db(query, data)