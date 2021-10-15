from flask import Flask
from gobowls_app import app
from gobowls_app.controllers import users_controller, bowls_controller, orders_controller

if __name__ == '__main__':
    app.run(debug=True)
