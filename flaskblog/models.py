from datetime import datetime
from flaskblog import db, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def loadUser(userId):
    return User.query.get(int(userId))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique= True, nullable = False)
    email = db.Column(db.String(120), unique= True, nullable = False)
    image_file = db.Column(db.String(20), unique=False, nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable = False)

    posts = db.relationship('Post', backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.image_file}', '{self.password}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), unique= False, nullable = False)
    content = db.Column(db.Text, unique=False, nullable=False)
    datePosted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.author}', '{self.title}', '{self.datePosted}')"