''' Models for Notes app'''
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    ''' Connect to databse'''
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User.'''

    __tablename__ = 'users'

    username = db.Column(db.String(20),
                primary_key=True)
    password = db.Column(db.String(),
                nullable = False)
    email = db.Column(db.String(50),
                nullable = False)
    first_name = db.Column(db.String(30),
                nullable = False)
    last_name = db.Column(db.String(30),
                nullable = False)

    def __repr__(self):
        ''' Return info about the user'''
        return f'<User {self.username}, first name {self.first_name}, last name {self.last_name}, email {self.email}>'
                
    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd).decode('utf8')

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed)

    @classmethod
    def authenticate(cls,username,pwd):
        """ Validate that username exists and password is correct
        Return user if valid; relse return false.
        """

        u = User.query.filter(User.username==username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

    @classmethod
    def authorized(cls, username, userid_in_session):
        """ Check if the user is authorized """

        return userid_in_session == username
            