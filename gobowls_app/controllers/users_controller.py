from flask import Flask, render_template, redirect, session, request
from gobowls_app import app
from gobowls_app.models.users import User
from gobowls_app.models import orders

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/', methods=['POST', 'GET'])
def home():
    if not 'userid' in session:
        return render_template('index.html')
    return redirect ('/dashboard')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if not 'userid' in session:
        return render_template ('login.html')
    return redirect ('/dashboard')

@app.route('/register', methods=['POST'])
def registration():
    print (request.form)
    if not User.register_validation(request.form):
        return redirect ('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    user = User.register_user(data)
    location = {
        'user_id' : user,
        'address' : request.form['address'],
        'city' : request.form['city'],
        'state' : request.form['state']
    }
    address = User.register_address(location)
    session['userid'] = user
    session['orders'] = 0
    return redirect ('/dashboard')    

@app.route('/userlogin', methods=['POST'])
def userlogin():
    if not User.login_validation(request.form):
        return redirect ('/login')
    return redirect ('/dashboard')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not 'userid' in session:
        return redirect ('/')
    return render_template ('home.html', info = session)

@app.route('/logout', methods=['GET'])
def restart():
    remove = orders.Order.closession()
    session.clear()
    return redirect('/')