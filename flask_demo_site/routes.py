from flask import render_template, redirect, url_for, flash, request
from flask_demo_site import app, mysql
from flask_demo_site.forms import RegisterForm, LoginForm
# from flask_demo_site.models import User

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", title="Home")

@app.route('/about')
def about():
    return render_template("about.html", title="About")

@app.route('/account')
def account():
    return render_template("account.html", title="Account")

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            username = request.form['username'],
            email = request.form['email'],
            password = request.form['password'],
            cur = mysql.connection.cursor()
            print("User : ", username) 
            print("Email : ", email)
            print("Password : ", password) 
            
            cur.execute("INSERT INTO users (username, email_address, password) VALUES (%s,%s,%s)", (username, email, password) )
            mysql.connection.commit()
            reg_cur.close()
            
            flash(f'Account created succesfully', category='success')
            return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)

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

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template(url_for('error_pages', filename= "404.html"), title="Page not found")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", title="Page not found"), 404

@app.errorhandler(403)
def forbiden(e):
    return render_template("403.html", title="Forbidden")

@app.errorhandler(410)
def does_not_exist(e):
    return render_template("410.html", title="Doesn't exist anymore")   

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", title="Internal server error")