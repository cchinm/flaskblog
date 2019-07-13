from app import db

class ReflectTab(db.Model):

    __tablename__='reflect_tab'

    tpe_id = db.Column(db.Integer, primary_key=True)
    tpe_name = db.Column(db.String)
    reflect_field = db.Column(db.String)