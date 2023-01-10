from datetime import datetime 
from flask import Flask, url_for, render_template, flash, redirect, request
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import os
from os import path

# creating a flask instance
blog = Flask(__name__)
base_dir=os.path.dirname(os.path.realpath(__file__))
# adding database
blog.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir,'bloggers.db')
# blog.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogdata.db'
blog.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
# secret key
blog.config['SECRET_KEY'] = '12345678'

# initialize the database
db = SQLAlchemy(blog)
db.blog=blog
# flask-SQLAlchemy versions from 3.0 require an active flask blog context before accesing db.session or db.engine
with blog.app_context():
    db.create_all()

class Contributor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    image_file = db.Column(db.String, nullable=True, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"Contributor('{self.username}', '{self.last_name}', '{self.last_name}', '{self.email}', '{self.image_file}')"

class Writers(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    first_name=db.Column(db.String(30),nullable=True)
    last_name=db.Column(db.String(30),nullable=True)
    username=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(30),nullable=False)
    age=db.Column(db.Integer())
    gender=db.Column(db.String())
    password=db.Column(db.String())
    confirm_password=db.Column(db.String())
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"Contributors {self.username}"

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



@blog.route("/")
@blog.route("/home")
def home():
    return render_template('home.html', posts=all_posts)


@blog.route("/about")
def about():
    return render_template('about.html', title='About')

@blog.route('/negritude')
def afrostreet():
    return "afro edition of life"


@blog.route("/signup", methods=['GET', 'POST'])
def register():
    form=RegistrationForm()

    if request.method == "POST":
        
        # username=request.form.get('username')
        # email=request.form.get('email')
        # password=request.form.get('password')
        # confirm_password=request.form.get('confirm_password')
        # age=request.form.get('age')
        # first_name=request.form.get('first_name')
        # last_name=request.form.get('last_name')
        # gender=request.form.get('gender')

        # new_writer=Writers(
        #     first_name=first_name,
        #     last_name=last_name,
        #     username=username,
        #     age=age,
        #     password=password,
        #     email=email,
        #     gender=gender,
        #     confirm_password=confirm_password
        # )

        if form.validate_on_submit():
            flash('Account created!', 'success')
            
        
        return redirect(url_for('home'))
        return "signed up and validated successfully"
           
        new_user = Contributor(email=form.email.data, username=form.username.data, password=form.password.data)
        # db.session.add(new_writer)
        db.session.commit

         
    return render_template('signup.html', form=form)



@blog.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
        
         return redirect(url_for('home'))
         flash('You have been logged in!', 'success')
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# demonstrating a personalised welcome page
@blog.route('/home/<string:name>')
def pesrsonalisedhome(name):
    return "Welcome to main blog, dear " + name    


@blog.route('/posts', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', post=all_posts)


@blog.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@blog.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


@blog.route('/users', methods=['POST'])
def create_user():
    username=request.form.get('username')
    email=request.form.get('email')
    age=request.form.get('age')
    gender=request.form.get('gender')

    print(f"{username} {email} {age} {gender}")

    new_user=User(username=username,
        email=email,
        age=age,
        gender=gender
    )
    db.session.add()
    db.session.commit(new_user)

    return redirect(url_for('home'))

    return "submitted"


if __name__ == '__main__':
    blog.run(debug=True)

