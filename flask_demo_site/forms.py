from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp

class RegisterForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[DataRequired(),
                                       Length(min=3, max=30),
                                       Regexp("^[a-z0-9]+$")
                                       ])
    email = StringField(label='Email address',
                        validators=[DataRequired(),
                                    Email()
                                    ])
    password = PasswordField(label='Password',
                             validators=[DataRequired(),
                                         Length(min=6, max=40)
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
                             validators=[DataRequired(),
                                         Length(min=6, max=40)
                                         ])
    submit = SubmitField(label='Login')