from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_demo_site import app, mysql, login_manager
from flask_demo_site.forms import RegisterForm, LoginForm, VerifyEmailForm, ResetPasswordForm
from flask_demo_site.helpers.random_alphanum_str import generate_aplhanum_str
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, LoginManager, login_user, logout_user
from config import config
from datetime import timedelta

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return User(*cursor.fetchone())


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

def check_existing_email(email):
    conn_cursor = mysql.connection.cursor()
    conn_cursor.execute("""SELECT password FROM users 
                        WHERE email_address = '{}'""".format(email))
    result = conn_cursor.fetchone()
    return result

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        
        username = str(generate_aplhanum_str(10)) 
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, config['HASH_METHOD'])
        
        precheck = check_existing_email(email)
        if precheck:
            flash(f'User already exist', category= 'warning')
        else:
            conn_cursor = mysql.connection.cursor()
            conn_cursor.execute("""INSERT INTO users (
                username, user_first_name, user_last_name, email_address, password)
                VALUES (%s,%s,%s,%s,%s)""", (username, fname, lname, email, hashed_password))
            mysql.connection.commit()
            conn_cursor.close()
            user = check_existing_email(email)
            if user:
                session['loggedin'] = True
                session['email'] = email
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
        
        user = check_existing_email(email)
        if user and check_password_hash(user[0], password):
            session['loggedin'] = True
            session['email'] = email
            flash(f'Logged in succesfully', category='success')
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

@app.route('/username_check', methods=['POST'])
def username_check():
    conn = None
    cursor = None
    try:
        username = request.form.get('username')
        if username and request.method == 'POST':
            conn_cursor = mysql.connection.cursor()
            conn_cursor.execute("""SELECT * FROM users 
                                WHERE username = '{}'""".format(username))
            row = conn_cursor.fetchone() 
            
            if row:
                response = jsonify('<span style="color: red">Username unavailable</span>')
                response.status_code = 200
                return response
            else:
                response = jsonify('<span style="color: red">Username available</span>')
                response.status_code = 200
                return response        
        else:
            response = jsonify('<span style="color: red">Username is required</span>')
            response.status_code = 200
            return response        
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

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