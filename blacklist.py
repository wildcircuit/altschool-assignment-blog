from flask import Flask, render_template, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


class Blacklist():
    __tablename__ ='blacklist'
    id = db.Column(db.Intger, primary_key=True, autoincrement=True)
    token = db.Column(db.Integer, unique=True, nullable=False)
    blacklisted_on = db.Column(db.datetime, nullable=False)

    def __init__(self,token: str):
        self.token = token
        self.blacklisted_on = datetime.now()

        def __repr__(self):
            return '<id: token: {}>' .format(self.token)

class Blogpost():
    __tablename__=
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60))
    subtitle =
    author = db.Column(db.String(40), nullable=False)
    date_posted = db.Column(db.datetime)
    content = 


@staticmethod
def check_blacklist(auth_token) -> bool:
    result = Blacklist.query_filter_by(token = str(auth_token).first())
    if result:
        return True
    else:
        return False


@app.route(/)
def index():
    posts = 

    return render_template()