from flask import Flask
from os import environ
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']


from routes import *
if __name__ == '__main__':
    app.run()
