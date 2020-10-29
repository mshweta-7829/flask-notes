from app import app
from models import db, User

db.drop_all()
db.create_all()

u1 = User(
    username='User1', 
    password='Password1', 
    email ='Email1@email.com', 
    first_name='FirstName1', 
    last_name = 'LastName1')
u2 = User(
    username='User2', 
    password='Password2', 
    email ='Email2@email.com', 
    first_name='FirstName2', 
    last_name = 'LastName2')

db.session.add_all([u1,u2])
db.session.commit()