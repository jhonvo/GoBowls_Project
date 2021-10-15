from flask import Flask, render_template, redirect, session, request
from gobowls_app import app
from gobowls_app.models.orders import Order

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/neworder', methods=['POST', 'GET'])
def neworder():
    if not 'userid' in session:
        return redirect ('/')
    return render_template ('neworder.html')

@app.route('/orders', methods=['POST', 'GET'])
def orders():
    if not 'userid' in session:
        return redirect ('/')
    return render_template ('orders.html')

@app.route('/account', methods=['POST', 'GET'])
def account():
    if not 'userid' in session:
        return redirect ('/')
    return render_template ('account.html')


@app.route('/favorites', methods=['POST', 'GET'])
def favorites():
    if not 'userid' in session:
        return redirect ('/')
    return render_template ('favorites.html')

@app.route('/randomorder', methods=['POST', 'GET'])
def randomorder():
    if not 'userid' in session:
        return redirect ('/')
    return render_template ('randomorder.html')