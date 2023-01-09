from flask import render_template
from flask_demo_site import app

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", title="Home")

@app.route('/about')
def anout():
    return render_template("about.html", title="About")

@app.route('/login')
def login():
    return render_template("login.html", title="Login")

@app.route('/register')
def register():
    return render_template("register.html", title="Register")