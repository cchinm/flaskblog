from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):

    __tablename__ = "blog_user"
    user_id = db.Column('id', db.Integer, primary_key=True)
    password = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(20), unique=True)



    def __init__(self, user_id=None, account_number=None, password=None, name="anonymous"):
        self.user_id = user_id
        self.password = password
        self.name = name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return "%d" % self.user_id

    def __repr__(self):
        return '<User %r>' % (self.user_id)

