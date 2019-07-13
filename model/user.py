from app import db



class UserForm(db.Model):
    __tablename__ = "blog_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    # pass


class UserIpRecord(db.Model):
    __tablename__ = "user_ip_record"
    id = db.Column(db.Integer, primary_key=True)
    user_ip = db.Column(db.String)
    user_visit_time = db.Column(db.DateTime)
    visit_router = db.Column(db.String)



