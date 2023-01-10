from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from xmlrpc.client import Boolean
from wtforms.validators import DataRequired, Length, EqualTo



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20, message="you are not within character range")])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="passwords do not match")])
    submit = SubmitField(label='Sign Up')
    first_name = StringField('first_name', validators={DataRequired(), Length(min=4, max=20, message="you are outside character range")})
    last_name = StringField('last_name', validators={DataRequired(), Length(min=4, max=20, message="you are outside character range")})
    age=StringField('age')
    gender=StringField('gender')

    # def validate_username(self, username):
    #     new_cont = Contributor.query.filter_by(username=username.data).first()
    #     if new_cont:
    #         raise ValidationError('username already taken')

class UserForm(FlaskForm):
    first_name = StringField('Firstname')
    last_name = StringField('Lastname')
    submit = SubmitField('Edit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First Name')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=12)])
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


# <!-- <form action="{{url_for('register')}}" method="POST">
#     {{ form.hidden_tag() }}
#     <fieldset>
#             <legend>Become a Contributor Today</legend>


# <br>
# <br>
#             <div>
#                 {{ form.first_name.label }}
#                 {% if form.first_name.errors %}
#                     {{ form.first_name(class="is-invalid") }}
#                         <div>
#                             {% for error in form.first_name.errors %}
#                                 <small class="error">{{ error }}</small>
#                             {% endfor %}
#                         </div>
#                 {% else %}
#                     {{ form.first_name }}
#                 {% endif %}
#             </div>
#             <div>
#                 {{ form.last_name.label }}
#                 {% if form.last_name.errors %}
#                     {{ form.last_name(class="is-invalid") }}
#                         <div>
#                             {% for error in form.last_name.errors %}
#                                 <small class="error">{{ error }}</small>
#                             {% endfor %}
#                         </div>
#                 {% else %}
#                     {{ form.last_name }}
#                 {% endif %}
#             </div>
#             <div>
#                 {{ form.username.label }}
#                 {% if form.username.errors %}
#                     {{ form.username(class="is-invalid") }}
#                         <div>
#                             {% for error in form.username.errors %}
#                                 <small class="error">{{ error }}</small>
#                             {% endfor %}
#                          </div>
#                 {% else %}
#                     {{ form.username }}
#                 {% endif %}
#             </div>
#             <div>
#                 {{ form.email.label }}
#                 {% if form.email.errors %}
#                     {{ form.email(class="is-invalid") }}
#                         <div>
#                             {% for error in form.email.errors %}
#                                 <small>{{ errors }}</small>
#                             {% endfor %}
#                          </div>
#                 {% else %}
#                     {{ form.email }}
#                 {% endif %}
#             </div>
#             <div>
#                 {{ form.age.label }}
#                 {% if form.age.errors %}
#                     {{ form.age(class="is-invalid") }}
#                         <div>
#                             {% for error in form.age.errors %}
#                                 <small>{{ errors }}</small>
#                             {% endfor %}
#                          </div>
#                 {% else %}
#                     {{ form.age }}
#                 {% endif %}
#             </div>
#             <div>
#                 {{ form.gender.label }}
#                 {% if form.gender.errors %}
#                     {{ form.gender(class="is-invalid") }}
#                         <div>
#                             {% for error in form.gender.errors %}
#                                 <small>{{ errors }}</small>
#                             {% endfor %}
#                          </div>
#                 {% else %}
#                     {{ form.gender }}
#                 {% endif %}
#             </div>
#             <div>
#                 {{ form.password.label }}
#                 {% if form.password.errors %}
#                     {{ form.password(class="is-invalid") }}
#                         <div>
#                             {% for error in form.password.errors %}
#                                 <span class="error">{{ error }}</span>
#                             {% endfor %}
#                          </div>
#                 {% else %}
#                     {{ form.password }}
#                 {% endif %}
#             </div>
#             <div>
#                 {{ form.confirm_password.label }}
#                 {% if form.confirm_password.errors %}
#                     {{ form.confirm_password(class="is-invalid") }}
#                         <div>
#                             {% for error in form.confirm_password.errors %}
#                                 <small class="error">{{ error }}</small>
#                             {% endfor %}
#                          </div>
#                 {% else %}
#                     {{ form.confirm_password }}
#                 {% endif %}
#             </div>
#     </fieldset>
#     <div>
#     {{ form.submit }}
#     </div>
# </form> -->