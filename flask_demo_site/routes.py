from flask import render_template, redirect, url_for, flash, request, session
from flask_demo_site import app, mysql
from flask_demo_site.forms import RegisterForm, LoginForm, VerifyEmailForm, ResetPasswordForm
from flask_demo_site.helpers.random_num_str import generate_num_str
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, LoginManager, login_user, logout_user
from config import config
from datetime import timedelta
# hashed_password = generate_password_hash(password, salt=salt)

# is_match = check_password_hash(hashed_password, password)
# print(is_match)


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

def fetch_existing_user(email, password):
    conn_cursor = mysql.connection.cursor()
    conn_cursor.execute("""SELECT password FROM users 
                        WHERE email_address = '{}'""".format(email))
    result = conn_cursor.fetchone()
    # if result and check_password_hash(result[0], password):
    #     conn_cursor.execute("""SELECT  FROM users 
    #                     WHERE email_address = '{}'""".format(email))
    #     result = conn_cursor.fetchone()
    return result

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
            
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        email = request.form.get('email')
        username = "user"+str(generate_num_str(8))
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, config['HASH_METHOD'])
                
        conn_cursor = mysql.connection.cursor()
        conn_cursor.execute("""INSERT INTO users (
            username, user_first_name, user_last_name, email_address, password)
            VALUES (%s,%s,%s,%s,%s)""", (username, fname, lname, email, hashed_password))
        mysql.connection.commit()
        conn_cursor.close()
        
        user = fetch_existing_user(email, password)
        
        if user:
            session['loggedin'] = True
            session['email'] = email
            session['user'] = user[0][0]
            flash(f'Account created succesfully', category='success')
            return redirect(url_for('account'))
    return render_template("register.html", title="Register", form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
    
        email = request.form.get('email')
        password = request.form.get('password')
        rememberme = True if request.form.get('rememberMe') else False
        
        user = fetch_existing_user(email, password)
        
        if user and check_password_hash(user[0], password):
            print("User logged in successfully")
            return redirect('home')
        else:
            flash(f'Login failed', category='danger') 
    return render_template("login.html", title="Login", form=form)

@app.route('/forgot-password', methods=['POST', 'GET'])
def verify_email():
    form = VerifyEmailForm()
    if form.validate_on_submit() and request.method == 'POST':
    
        email = request.form.get('email')
        
        conn_cursor = mysql.connection.cursor()
        conn_cursor.execute("SELECT * FROM users WHERE email_address LIKE '{}'".format(email))
        user = conn_cursor.fetchall()
        if user:
            flash(f'Please check your email for password reset link.', category='info')
        else:
            flash(f'Found no such account. ', category='danger')
            
    return render_template("verify_email.html", title="Login", form=form)

@app.route('/reset-password', methods=['POST', 'GET'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit() and request.method == 'POST':
    
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn_cursor = mysql.connection.cursor()
        conn_cursor.execute("SELECT * FROM users WHERE email_address LIKE '{}' AND password LIKE '{}'".format(email, password))
        user = conn_cursor.fetchall()
        if user:
            session['user'] = user[0][0]
            print(user[0][0])
        else:
            flash(f'Login failed', category='danger') 
    return render_template("login.html", title="Login", form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('email', None)
    session.pop('loggedin', None)
    return redirect('login')

# Error handling pages
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