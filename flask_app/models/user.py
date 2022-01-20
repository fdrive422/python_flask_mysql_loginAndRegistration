from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app import app # NEEDED FOR BCRYPT!!
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 


class User:
    db_name = 'login_and_registration_schema'  # class variable should match dB schema name
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # Method to register 'save' anew user
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result


    # Method to select/show a user
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print(result)
        return cls(result[0])


    # Method to select and display user
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        return cls(result[0])


    # Static method to validate user registration inputs
    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['first_name']) < 2:
            is_valid = False
            flash('*First name must be at least two characters', 'register_errors')
        if len(data['last_name']) < 2:
            is_valid = False
            flash('*Last name must be at least two characters', 'register_errors')
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('*Invalid email address', 'register_errors')
        elif User.validate_login(data):
            is_valid = False
            flash(f"*{data['email']} is already in use on this site", 'register_errors')
        if len(data['password']) < 8:
            is_valid = False
            flash('*Passwords must be at least eight characters', 'register_errors')
        if len(data['confirm_password']) < 8:
            is_valid = False
            flash('*Passwords must be at least eight characters', 'register_errors')
        elif data['password'] != data['confirm_password']:
            is_valid = False
            flash('*Passwords do not match', 'errors')
        return is_valid


    # Static method to validate login information
    @staticmethod
    def validate_login(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query, data)
        if len(results) < 1:
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
        if is_valid:
            is_valid = True
        return is_valid