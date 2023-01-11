from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY']='firstflask123'
from flask_demo_site import routes