from gobowls_app.config.mysqlconnection import connectToMySQL
from gobowls_app import app
from flask import flash, session

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @staticmethod
    def register_validation(data):
        is_valid = True
        user = User.get_by_email(data)
        if len(user) > 0:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Please provide a valid email address.","register")
            is_valid=False
        if len(data['first_name']) <3:
            flash("First name should be more than 3 characters.","register")
            is_valid=False
        if len(data['last_name']) < 3:
            flash("Last name should be more than 3 characters.","register")
            is_valid=False
        if len(data['address']) < 3:
            flash("Address should be more than 3 characters.","register")
            is_valid=False
        if len(data['city']) < 3:
            flash("City should be more than 3 characters.","register")
            is_valid=False
        if data['state'] == "None":
            flash("Please select a valid state.","register")
            is_valid=False
        if len(data['password']) < 8:
            flash("Password should include more than 8 characters.","register")
            is_valid=False
        if data['password'] != data['password_confirmation']:
            flash("Passwords do not match, please review.","register")
            is_valid=False
        return is_valid

    @staticmethod
    def login_validation(data):
        is_valid = True
        user = User.get_by_email(data)
        if len(user) < 1:
            flash("Email not valid.","login")
            is_valid=False
        elif not bcrypt.check_password_hash(user[0].password, data['password']):
            flash("Incorrect password, please try again.","login")
            is_valid=False
        else:
            session['userid'] = user[0].id
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('gobowls').query_db(query,data)
        user = []
        for line in results:
            user.append(User(line))
        return user
    
    @classmethod
    def register_user(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        results = connectToMySQL('gobowls').query_db(query,data)
        return results

    @classmethod
    def register_address(cls,data):
        query = "INSERT INTO addresses (user_id,address,city,state) VALUES (%(user_id)s,%(address)s,%(city)s,%(state)s);"
        results = connectToMySQL('gobowls').query_db(query,data)
        return results