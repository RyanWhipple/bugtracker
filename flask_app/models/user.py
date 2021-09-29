from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.thoughts = []
        self.likes  =   []


    # Validate User Registration
    @staticmethod
    def validate_registration(user, methods=["POST"]):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if len(user['email']) < 8:
            flash("Email must be at least 8 characters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if user['password'] != user['password_confirm']:
            flash("Password and Confirm Password do not match")
            is_valid_ = False
        if not any(char.isdigit() for char in user['password']):
            flash("Password requires at least one digit 0-9")
            is_valid = False
        if not any(char.isupper() for char in user['password']):
            flash("Password requires at least one upper case character A-Z")
            is_valid = False

        return is_valid


    # Validate User Update
    @staticmethod
    def validate_update(user, methods=["POST"]):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if len(user['email']) < 8:
            flash("Email must be at least 8 characters.")
            is_valid = False

        return is_valid


    # Save User
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s ) "
        print("returning from save()")
        return connectToMySQL().query_db(query, data)


    # Update User
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email=%(email)s WHERE id = %(id)s "
        print("returning from update()")
        return connectToMySQL().query_db(query, data)


    # Get User by ID
    @classmethod
    def get_by_id(cls, data):
        data = {
            'id'    : session['user_id']
        }
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL().query_db(query, data)
        print("returning from get_by_id()")
        return results[0]


    # Get User by Email
    @classmethod
    def get_by_email(cls, data):
        print("running get_by_email()")
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL().query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])