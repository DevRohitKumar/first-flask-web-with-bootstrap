from flask import Flask
from flask_mysqldb import MySQL
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from config import config


app = Flask(__name__)

app.config['SECRET_KEY'] = config['SECRET_KEY']
app.permanent_session_lifetime = config['PERMANENT_SESSION_LIFETIME']
serializer = URLSafeTimedSerializer(config['SECRET_KEY'])

app.config['MYSQL_HOST'] = config['DATABASE_URL']
app.config['MYSQL_USER'] = config['DATABASE_USERNAME']
app.config['MYSQL_PASSWORD'] = config['DATABASE_PASSWORD']
app.config['MYSQL_DB'] = config['DATABASE']

app.config['MAIL_SERVER'] = config['MAIL_SERVER']
app.config['MAIL_PORT'] = config['MAIL_PORT']
app.config['MAIL_USE_SSL'] = config['MAIL_USE_SSL']
app.config['MAIL_USE_TLS'] = config['MAIL_USE_TLS']
app.config['MAIL_USERNAME'] = config['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config['MAIL_PASSWORD']


mysql = MySQL(app)
mail = Mail(app)




from flask_demo_site import routes