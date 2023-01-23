from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp

class RegisterForm(FlaskForm):
    firstname = StringField(label="First Name",
                        validators=[DataRequired(),
                                    Length(min=3, max=20),
                                    Regexp("^[a-zA-Z]+$")
                                    ])
    lastname = StringField(label="Last Name",
                        validators=[DataRequired(),
                                    Length(min=3, max=20),
                                    Regexp("^[a-zA-Z]+$")
                                    ])
    email = StringField(label='Email address',
                        validators=[DataRequired(),
                                    Email()
                                    ])
    password = PasswordField(label='Password',
                             validators=[DataRequired(),
                                         Length(min=6, max=52),
                                         Regexp("^[a-zA-Z0-9]+$"),
                                        #  Regexp("/^[\x21-\x7E]+$/"),
                                         #  Regexp("/^[\w.~`!@#$%^&*()-+=<>?,\/\[\]\{\}\|]+$/")
                                         ])
    confirm_password = PasswordField(label='Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password', 
                                                         message="Password does not match.")
                                                 ])
    submit = SubmitField(label='Join Now')
    
class LoginForm(FlaskForm):
    email = StringField(label='Email address',
                        validators=[DataRequired(),
                                    Email()
                                    ])
    password = PasswordField(label='Password',
                             validators=[DataRequired()])
    rememberMe = BooleanField(label="Keep me logged in",
                              default=False)
    submit = SubmitField(label='Login')
    
class VerifyEmailForm(FlaskForm):
    email = StringField(label="Your Email Address",
                      validators= [DataRequired(),
                                   Email(),
                                   ])
    submit = SubmitField(label="Send verification link")
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='New Password',
                             validators=[DataRequired(),
                                         Length(min=6, max=40)
                                         ])
    confirm_password = PasswordField(label='Confirm New Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password',
                                                         message="Password does not match."
                                                        )
                                                 ])
    submit = SubmitField(label='Reset Password')
    