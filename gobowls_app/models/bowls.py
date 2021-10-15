from gobowls_app.config.mysqlconnection import connectToMySQL
from gobowls_app import app
from flask import flash, session

import re
NUMBER_REGEX = re.compile(r'^[0-9]+$')

class Bowl:
    def __init__(self,data):
        self.id = data['id']
        self.method = data['method']
        self.size = data['size']
        self.base = data['base']
        self.quantity = data['quantity']
        self.dressing = data['dressing']
        self.price = data['price']

    @staticmethod
    def order_validation(data):
        is_valid = True
        ingredient = 0
        if data['method'] == "None":
            flash("Please select a valid method.")
            is_valid=False
        if data['size'] == "None":
            flash("Please select a valid size.")
            is_valid=False
        if data['base'] == "None":
            flash("Please select a valid base.")
            is_valid=False
        if data['dressing'] == "None":
            flash("Please select a valid dressing.")
            is_valid=False
        if not NUMBER_REGEX.match(data['quantity']) or int(data['quantity']) <= 0:
            flash("Quantity should be 1 or more.")
            is_valid=False
        for element in data:
            if 'ingredient' in element:
                ingredient += 1
        if ingredient == 0:
            flash("Please select at least one ingredient.")
            is_valid=False
        return is_valid
    
    @classmethod
    def newbowl(cls, data):
        query = "INSERT INTO bowls (method, size,base,quantity,dressing,order_id) VALUES (%(method)s, %(size)s,%(base)s,%(quantity)s,%(dressing)s,%(order_id)s);"
        bowl = connectToMySQL('gobowls').query_db(query,data)
        return bowl

    @classmethod
    def saveingredient(cls,data):
        query = "INSERT INTO bowl_ingredients (ingredient_id, bowl_id) VALUES (%(ingredient_id)s,%(bowl_id)s);"
        ingredient = connectToMySQL('gobowls').query_db(query,data)
        return ingredient

    @classmethod
    def sumofvalues(cls,id):
        query =  "SELECT sum(ingredients.price) as sum FROM ingredients LEFT JOIN bowl_ingredients ON bowl_ingredients.ingredient_id = ingredients.id WHERE bowl_id = %(id)s;"
        data = {
            'id' : id
        }
        sum = connectToMySQL('gobowls').query_db(query,data)
        return sum

    @classmethod
    def updateprice(cls,data):
        query = "UPDATE bowls SET price = %(price)s WHERE id = %(id)s"
        update = connectToMySQL('gobowls').query_db(query,data)
        return update