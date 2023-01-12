from flask import render_template, redirect, url_for, flash
from flask_demo_site import app
from flask_demo_site.forms import RegisterForm, LoginForm

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", title="Home")

@app.route('/about')
def about():
    return render_template("about.html", title="About")

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'admin123':
            flash(f'Login successful', category='success')
            return redirect(url_for('home'))
        else:
            flash(f'Login failed', category='danger')
    return render_template("login.html", title="Login", form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'Account created succesfully', category='success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)

@app.route('/account')
def account():
    return render_template("account.html", title="Account")