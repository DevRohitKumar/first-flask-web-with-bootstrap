from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
 
app = Flask(__name__)

app.config['SECRET_KEY']='firstflask123'
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/demosite.db"
# db = SQLAlchemy(app)
# db.init_app(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_demo_db'
 
mysql = MySQL(app)
   
from flask_demo_site import routes