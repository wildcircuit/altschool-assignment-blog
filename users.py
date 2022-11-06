from flask import Flask

from sqlalchemy.sql import func



class User(db.models):
    __table_name__="users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(40))
    username = db.Column(db.String(40))
    email = db.Column(db.String(50, unique=True))
    registered_on = db.Column(db.DateTime, default=func.now())
    updated_on = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(50))
    roles = db.relationship('Roles',secondary='user_roles', backref=('Users', lazy='joined'), uselist=False)

    def __repr__(self) -> str:
        return '<User %r>' % self.username

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Blog
    

class Role(db.models):
    __tablename__ = "Roles"
    id = db.Column(db.Integer, primarykey=True, autoincrement=True)
    role = db.Column(db.String(39), unique=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserRoles(db.model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer,primarykey=True, autoincrement=True)
    user_id = db.Column(db.Integer(39), db.Foreignkey(user.id, ondelete='CASCADE'))
    role_id = db.Column(db.Integer(39), db.Foreignkey(role.id, ondelete='CASCADE'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

        