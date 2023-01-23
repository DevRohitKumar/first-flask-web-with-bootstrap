from flask import Flask
from flask_mysqldb import MySQL
from config import config
app = Flask(__name__)

app.config['SECRET_KEY'] = config['SECRET_KEY']
app.permanent_session_lifetime = config['PERMANENT_SESSION_LIFETIME']

app.config['MYSQL_HOST'] = config['DATABASE_URL']
app.config['MYSQL_USER'] = config['DATABASE_USERNAME']
app.config['MYSQL_PASSWORD'] = config['DATABASE_PASSWORD']
app.config['MYSQL_DB'] = config['DATABASE']

mysql = MySQL(app)


from flask_demo_site import routes