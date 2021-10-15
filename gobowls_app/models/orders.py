from gobowls_app.config.mysqlconnection import connectToMySQL
from gobowls_app import app
from flask import flash, session

class Order:
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.confirmed_at = data['confirmed_at']

    @classmethod
    def neworder(cls):
        query = "INSERT INTO orders (user_id) VALUES (%(user_id)s);"
        data = {
            'user_id' : session['userid']
        }
        order = connectToMySQL('gobowls').query_db(query,data)
        return order

    @classmethod
    def closession(cls):
        query = "DELETE FROM orders WHERE user_id = %(id)s AND orders.confirmed_at IS NULL;"
        data = {
            'id' : session['userid']
        }
        return connectToMySQL('gobowls').query_db(query,data)