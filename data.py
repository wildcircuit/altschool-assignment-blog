from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user


base_dir=os.path.dirname(os.path.realpath(__file__))
# creating a flask instance
data = Flask(__name__)
# adding database
data.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'contributors.db')
data.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
data.config["SECRET_KEY"]='84ab8b48cc44f56b9a'
# initializing the database
db = SQLAlchemy(data)
login_manager=LoginManager(data)

# setting up the structure of the database and the credential list
class Contributors(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    first_name=db.Column(db.String(30),nullable=False)
    last_name=db.Column(db.String(30),nullable=False)
    username=db.Column(db.String(),nullable=False,unique=True)
    email=db.Column(db.String(30),nullable=False,unique=True)
    age=db.Column(db.Integer(),nullable=True)
    gender=db.Column(db.String(),nullable=True)
    # password=db.Column(db.Text(),nullable=True)
    # confirm_password=db.Column(db.Text(),nullable=True)
    

    def __repr__(self):
        return f"Contributors {self.username}"

# class Users(db.Model):
#     id=db.Column(db.Integer(),primary_key=True)
#     first_name=db.Column(db.String(30),nullable=False)
#     last_name=db.Column(db.String(30),nullable=False)
#     username=db.Column(db.String(),nullable=False)
#     email=db.Column(db.String(30),nullable=False)
#     age=db.Column(db.Integer(),nullable=True)
#     gender=db.Column(db.String(),nullable=True)
#     password=db.Column(db.Text(),nullable=True)
#     confirm_password=db.Column(db.Text(),nullable=True)
    

#     def __repr__(self):
#         return f"Contributors {self.username}"

class BlogPost(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# opening page
@data.route("/", methods=['GET','POST'])
def welcome():
    return render_template('about.html')

# for managing a logged in session of contributor
@login_manager.user_loader
def user_loader(id):
    return Contributors.query.get(id)

# testing of display of signedform credentials
@data.route("/editors", methods=['POST', 'GET'])
def showeditors():
    contributors=Contributors.query.all()
    context={'contributors':contributors}
    return render_template('editors.html', **context)

# signing up and validating a contributor to blog
@data.route("/signup", methods=['GET', 'POST'])
def create_contributors():
    contributors=Contributors.query.all()
    if request.method=="POST":
        first_name=request.form.get("first_name")
        last_name=request.form.get("last_name")
        username=request.form.get("username")
        age=request.form.get("age")
        email=request.form.get("email")
        gender=request.form.get("gender")
        # confirm_password=request.form.get("confirm_password")
        # password=request.form.get("password")

        username_exists=Contributors.query.filter_by(username=username).first()

# checking for validity of contributors email, and username
        if username_exists:
            flash(f"username {username} is taken")
            return redirect(url_for('create_contributors'))

        email_exists=Contributors.query.filter_by(email=email).first()

        if email_exists:
            flash(f"email {email} is taken")
            return redirect(url_for('create_contributors'))

        # password_hash=generate_password_hash(password)

        new_contributor = Contributors(
            first_name=first_name,
            last_name=last_name,
            username=username,
            age=age,
            email=email,
            gender=gender
            # password=password,
            # confirm_password=confirm_password
        )
    

        db.session.add(new_contributor)
        db.session.commit()
        return redirect(url_for('login'))
    # return "submitted"
    context={'contributors':contributors}
    
    return render_template('signup.html',**context)

# logging in a blog contributor
@data.route('/login', methods=["GET","POST"])
def login():
    contributors=Contributors.query.all()
    username=request.form.get('username')
    password=request.form.get('password')

    user=Contributors.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return redirect(url_for('welcome'))

    return render_template('login.html', contributors=contributors,user=user)

# deleting a contributors loggedin session
@data.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('welcome'))

# updating a contributor's credentials
@data.route("/update/<int:id>/", methods=['GET', 'POST'])
def update(id):
    contributor_to_update = Contributors.query.get_or_404(id)

    
    if request.method == "POST":
        contributor_to_update.last_name=request.form.get('last_name')
        contributor_to_update.first_name=request.form.get('first_name')
        contributor_to_update.password=request.form.get('password')
        contributor_to_update.username=request.form.get('username')
        contributor_to_update.email=request.form.get('email')
        contributor_to_update.age=request.form.get('age')
        contributor_to_update.confirm_password=request.form.get('confirm_password')
        contributor_to_update.gender=request.form.get('gender')

        db.session.commit()
        return redirect(url_for('home'))
    
    context = {
        'contributor':contributor_to_update
    }
    return render_template('update.html',**context)

# deleting the list of signed up users/contributors
@data.route('/delete/<int:id>', methods=["GET"])
def delete_contributor(id):
    contributor_to_delete=Contributors.query.get_or_404(id)

    db.session.delete(contributor_to_delete)

    db.session.commit()

    return redirect(url_for('home'))



# generating details of blog posts
@data.route('/posts', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form.get('title')
        post_content = request.form['content']
        post_author = request.form['author']

        new_post = BlogPost(title=post_title, content=post_content, author=post_author)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        posts=BlogPost.query.all()
        # posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', post=posts)
     
# deleting posts in the blog
@data.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

# editing post contents of blog
@data.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
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


with data.app_context():
    db.create_all()

if __name__ == '__main__':
    data.run(debug=True)


