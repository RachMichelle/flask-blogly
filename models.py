from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

def connect_db(app):
    """connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """db user model"""
    __tablename__ = 'users'

    def __repr__(self):
        u=self
        return f"<User: {u.id} {u.first_name} {u.last_name} (image: {u.img_url})>"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    
    first_name = db.Column(db.String(25), nullable = False)

    last_name = db.Column(db.String(50), nullable = False)

    img_url = db.Column(db.String, nullable = False, default='https://t4.ftcdn.net/jpg/02/29/75/83/360_F_229758328_7x8jwCwjtBMmC6rgFzLFhZoEpLobB6L8.jpg')


    def get_full_name(self):
        u=self
        return f"{u.first_name} {u.last_name}"
    
class Post(db.Model):
    """db post model"""
    __tablename__ = 'posts'

    def __repr__(self):
        p=self
        return f"<Post {p.id}: Title-{p.title}, Content-{p.content}, Created at {p.created_at} by user id-{p.user_id}>"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    title = db.Column(db.Text, nullable = False)

    content = db.Column(db.Text, nullable = False)

    created_at = db.Column(db.DateTime, server_default = func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    usr = db.relationship('User', backref='psts')