from flask import Flask, render_template, redirect, session, request
from gobowls_app import app
from gobowls_app.models.bowls import Bowl
from gobowls_app.models import orders

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/addbowl', methods=['POST'])
def addbowl():
    # print (int(request.form['quantity']))
    if not Bowl.order_validation(request.form):
        return redirect ('/neworder')
    if not 'order_number' in session:
        order = orders.Order.neworder()
        session['order_number'] = order
    print ("This is Session", session)
    bowldata = {
        'method' : request.form['method'],
        'size' : request.form['size'],
        'base' : request.form['base'],
        'quantity' : request.form['quantity'],
        'dressing' : request.form['dressing'],
        'order_id' : session['order_number']
    }
    bowl = Bowl.newbowl(bowldata)
    for element in request.form:
        if 'ingredient' in element:
            ingredientdata = {
                'bowl_id' : bowl,
                'ingredient_id' : request.form[element]
            }
            ingredient = Bowl.saveingredient(ingredientdata)
    sumvalues = Bowl.sumofvalues(bowl)
    print ('This is SUM', sumvalues[0]['sum'])
    price = (float(sumvalues[0]['sum']) + 10) * int(request.form['quantity'])
    pricedata = {
        'id' : bowl,
        'price' : price
    }
    setprice = Bowl.updateprice(pricedata)
    return redirect ('/orders')