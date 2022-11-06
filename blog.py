from datetime import datetime 
from flask import Flask, url_for, render_template, flash, redirect, request
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from os import path

# creating a flask instance
app = Flask(__name__)

# adding database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogdata.db'
# secret key
app.config['SECRET_KEY'] = '12345678'

# initialize the database
db = SQLAlchemy(app)

# flask-SQLAlchemy versions from 3.0 requirean active flask app context before accesing db.sessionordb.engine
with app.app_context():
    db.create_all()

class Contributor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    image_file = db.Column(db.String, nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"Contributor('{self.username}', '{self.last_name}', '{self.last_name}', '{self.email}', '{self.image_file}')"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(60))

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.id}')"


class BlogPost(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('contributor.id'), nullable=False)

    def __repr__(self):
        return f"Contributors('{self.id}', '{self.title}', '{self.date_posted}')"


all_posts = [
    {
        'id': '001',
        'title': 'How it all started',
        'sub_title': 'the introduction of sapa101',
        'author': 'bach Anderson',
        'date_posted': 'October 30, 2022',
        'content': 'as we have begun this journey may it take us to beautiful places'
    },
    {
        'id': '002',
        'title': 'As we decide to carry on',
        'sub_title': 'the continuation of sapa101',
        'author': 'Ricardo Rodrigo',
        'date_posted': 'October 31, 2022' 'datetime.now',
        'content': 'we simply decided to try out this coding stuff and get good at it'       
    }
]



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=all_posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
         flash('You have been logged in!', 'success')
         return redirect(url_for('home'))
    else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)

