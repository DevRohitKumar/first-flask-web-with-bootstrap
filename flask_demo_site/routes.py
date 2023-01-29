from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_demo_site import app, mysql, mail, serializer
from flask_demo_site.forms import RegisterForm, LoginForm, VerifyEmailForm, ResetPasswordForm
from flask_demo_site.helpers.random_alphanum_str import generate_aplhanum_str
from werkzeug.security import generate_password_hash, check_password_hash
from config import config
from datetime import timedelta
from flask_mail import Message
from itsdangerous import SignatureExpired, BadSignature

def get_password_by_email(email):
    conn_cursor = mysql.connection.cursor()
    conn_cursor.execute("""SELECT password, email_verified FROM users 
                        WHERE email_address = '{}'""".format(email))
    result = conn_cursor.fetchone()
    return result

def get_user_by_email(email):
    conn_cursor = mysql.connection.cursor()
    conn_cursor.execute("""SELECT user_id, username, user_first_name, user_last_name 
                        FROM users WHERE email_address = '{}'""".format(email))
    result = conn_cursor.fetchone()
    return result

def set_user_session(userid, username, user_first_name, user_last_name):
    session['loggedin'] = True
    session['user'] = userid
    session['username'] = username
    session['fname'] = user_first_name
    session['lname'] = user_last_name

def send_email(mailing_route, email): 
    
    if mailing_route == "/register":
        token = serializer.dumps(email, salt="registration-confirmation")
        msg = Message("Demosite registration confirmation",
                      sender= 'demo_admin@demosite.com',
                      recipients=[email])
        
        link = url_for('registration_verification', token=token, _external=True)
        msg.html = render_template('confirm_registration_email_template.html', link= link)
        mail.send(msg)

###### Protected routes ######
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", title="Home")

@app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template("account.html", title="Account")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template("contact.html", title="Contact")

###### Posts routes ######
# @app.route('/post/<string:tab>', methods=['GET', 'POST'])
# def post(tab):
#     if tab == 'general':
#         return render_template('account.html'), tab

@app.route('/tab')
def tab():
    tab = request.args.get('tabId')    
    return render_template('account_'+tab+'.html')


###### Auth routes ######
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and request.method == 'POST':
        
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        userid = str(generate_aplhanum_str(15))
        username = email.split("@")[0]
        hashed_password = generate_password_hash(password, config['HASH_METHOD'])
        
        user_exist = get_user_by_email(email)
        if user_exist:
            flash(f'User already exist', category= 'warning')
        else:
            conn_cursor = mysql.connection.cursor()
            conn_cursor.execute("""INSERT INTO users (
                user_id, username, user_first_name, user_last_name, email_address, password)
                VALUES (%s, %s,%s,%s,%s,%s)""", (userid, username, fname, lname, email, hashed_password))
            mysql.connection.commit()
            conn_cursor.close()
                                    
            mailing_route = request.path
            send_email(mailing_route, email)
               
            flash(f'Verification email sent to {email}', category='success')
            session['new_user_email'] = email
            
            return redirect(url_for('register_verify_pending')), 301
    return render_template("register.html", title="Register", form=form)


@app.route('/verifaction/pending')
def register_verify_pending():
    email = session.get('new_user_email')
    return render_template('register_verify_pending.html', email = email)

@app.route("/register/verification/<token>")
def registration_verification(token):
    try:
        session.clear()
        token_email = serializer.loads(token, salt="registration-confirmation", max_age=3600)
        
        conn_cursor = mysql.connection.cursor()
        conn_cursor.execute(f"UPDATE users SET email_verified = '{1}' WHERE email_address = '{token_email}'")
        mysql.connection.commit()
        conn_cursor.close()
        
        new_user = get_user_by_email(token_email)
        set_user_session(new_user[0], new_user[1], new_user[2], new_user[3])
        return redirect(url_for('account'))
    except SignatureExpired:
        return "Token expired"
    except BadSignature:
        return "Invalid token"

@app.route('/login', methods=['POST', 'GET'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
    
        email = request.form.get('email')
        password = request.form.get('password')
        session.permanent = True if request.form.get('rememberMe') else False
        
        precheck = get_password_by_email(email)
        
        # Checking user credentials
        if precheck and check_password_hash(precheck[0], password):
            if precheck[1] == 0:
                return redirect(url_for('user_registered_not_verified'))
            
            user = get_user_by_email(email)
            set_user_session(user[0], user[1], user[2], user[3])
                        
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
        user = get_user_by_email(email)
        if user:
            flash(f'Please check your email for password reset request.', category='info')
        else:
            flash(f'Found no such account. ', category='danger')
            
    return render_template("verify_email.html", title="Login", form=form)

@app.route('/reset-password', methods=['POST', 'GET'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit() and request.method == 'POST':
    
        password = request.form.get('password')
        
        conn_cursor = mysql.connection.cursor()
        conn_cursor.execute("SELECT * FROM users WHERE email_address LIKE '{}' AND password LIKE '{}'".format(email, password))
        user = conn_cursor.fetchall()
        if user:
            session['user'] = user[0][0]
            print(user[0][0])
        else:
            flash(f'Login failed', category='danger') 
    return render_template("reset_password.html", title="Reset password", form=form)

@app.route('/logout')
def logout():
    session.clear()
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

###### User routes ######
# @app.route('/users/<str:username>/profile')
# def user_profile(username):
#     return render_template('user_profile.html', username=username)


###### General routes ######
@app.route('/terms')
def terms_and_conditions():
    return render_template("terms_and_conditions.html", title= "Terms and Conditions")

@app.route('/privacy')
def privacy():
    return render_template("privacy_policy.html", title= "Privacy Policy")

@app.route('/about')
def about():
    return render_template("about.html", title="About")


###### Error handling routes ######
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

###### Testing Route ######
@app.route('/testingroute')
def testingroute():
    return render_template("test.html", title="Testing")
