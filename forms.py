from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from xmlrpc.client import Boolean
from wtforms.validators import DataRequired, Length, EqualTo



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class UserForm(FlaskForm):
    first_name = StringField('Firstname')
    last_name = StringField('Lastname')
    submit = SubmitField('Edit')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')



# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[data_required(), Length(min=2, max=22)])
#     email = StringField('Email', validators=[data_required()])
#     password = PasswordField('Password', validators=[data_required()])
#     confirm_password = PasswordField('Password Confirmation', validators=[EqualTo('password'),data_required()])
#     submit = SubmitField('create account')


# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[data_required()])
#     password = PasswordField('Password', validators=[data_required()])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField('login')