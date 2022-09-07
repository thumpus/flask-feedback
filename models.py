from email.headerregistry import ParameterizedMIMEHeader
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """connect 2 database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    feedback = db.relationship("Feedback", backref="author", cascade="all, delete-orphan")


    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """returns registered user with hashed password"""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """validates that the user exists and password is correct. return user if valid, else return false"""
        lowered_username = username.lower()
        u = User.query.filter_by(username=lowered_username).first()
        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else: 
            return False

class Feedback(db.Model):
    __tablename__ = 'feedback'

    def __repr__(self):
        """show info about feedback"""
        f = self
        return f"id: {f.id} title: {f.title} content: {f.content} username = {f.username}"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.ForeignKey('users.username'), nullable=False)
