from app import db


class ArticleForm(db.Model):
    __tablename__ = "article_detail"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    post_time = db.Column(db.DateTime)
    md5_id = db.Column(db.String)
    post_author = db.Column(db.Integer)
    is_deleted = db.Column(db.Integer)
    short_summary = db.Column(db.String)
    is_priority = db.Column(db.Integer)
    views = db.Column(db.Integer)
    bg_img = db.Column(db.String)
    tags = db.Column(db.String)

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return '<User %s>' % self.title

    def to_json(self):
        di = self.__dict__
        if "_sa_instance_state" in di:
            del di['_sa_instance_state']
        return di


class ArticleContentForm(db.Model):
    __tablename__ = "blog_db"

    md5_id = db.Column(db.String, primary_key=True)
    tmp_content = db.Column(db.Text)

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return '<User %s>' % self.title

    def to_json(self):
        di = self.__dict__
        if "_sa_instance_state" in di:
            del di['_sa_instance_state']
        return di
