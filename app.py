import os
from flask import Flask
from flask_restful import Api

from flask_jwt import JWT
from security import authenticate, identity  # Flask-JWT requires these 2 functions to know how to handle an incoming JWT
                                             # and also what data we want to store in an outgoing JWT

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turn off flask-sqlalchemy modification tracker to free up resources
                                                     # because sqlalchemy has its own modification tracker
                                                     # this does not turn off sqlalchemy modification tracker
app.secret_key = 'jose' # app.secret_key is used to encode the JWT so you know it's your app that created it, not anyone else
                        # so that an end user cannot modify it in their browser
                        # Make this long, random, and secret in a real app
api = Api(app)

jwt = JWT(app, authenticate, identity) # as soon as we create a JWT object,
                                       # Flask-JWT registers an endpoint with our application, /auth

api.add_resource(UserRegister, '/register')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
