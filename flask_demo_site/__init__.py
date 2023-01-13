from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY']='firstflask123'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/demosite.db"

db = SQLAlchemy()
db.init_app(app)

    
from flask_demo_site import routes