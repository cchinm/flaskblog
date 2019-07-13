from flask import (Flask, jsonify,
                   render_template,
                   redirect,
                   request,
                   Markup,
                   send_from_directory)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, and_, or_

# from rdstools import  READ_COUNT, client

from markdown import markdown
from datetime import datetime
import traceback, re

from extensions import spider
from module.edit.edit_app import edit_page

app = Flask(__name__) # 新建app对象
app.register_blueprint(edit_page)
app.config.from_object('config') # 加载配置信息，其中有数据库的配置信息，包含在SQLALCHEMY_DATABASE_URI中

db = SQLAlchemy(app)
from models import ArticleForm, ArticleContentForm, UserForm, UserIpRecord

def record_ip(func):
    def wrap(*args, **kwargs):
        db.session.add(UserIpRecord(user_ip=request.remote_addr,
                                    user_visit_time=datetime.now(),
                                    visit_router=request.url))
        db.session.commit()
        return func(*args, **kwargs)
    return wrap

@app.route('/get', methods=['POST', 'GET'])
def hello_flask():
    db.session.add(UserIpRecord(user_ip=request.remote_addr,
                                user_visit_time=datetime.now(),
                                visit_router=request.url))
    db.session.commit()
    try:
        page = request.args.get('p') or '1'
        limit = request.args.get('count') or 10
        page = int(page)
        limit = 10 if int(limit) < 0 else int(limit)
        if limit > 10:
            limit = 10
        assert page >= 1
    except:
        page = 1
        limit = 10
    t = db.session.query(ArticleForm).filter(
        ArticleForm.is_deleted == 0
        ).order_by(desc(ArticleForm.is_priority), desc(ArticleForm.post_time)
                   ).limit(limit).offset((page-1)*10).all()

    tt = []
    for _ in t:
        author = db.session.query(UserForm.username).filter(UserForm.id ==_.post_author).first()
        tmp = _.to_json()
        tmp['post_author'] = author[0] if author else ''
        tmp['post_time'] = tmp['post_time'].strftime("%Y-%m-%d %H:%M:%S")
        # tmp['views'] = client.scard(READ_COUNT % tmp['md5_id']) + tmp['views']
        tt.append(tmp)
    print(page)
    return jsonify(tt)
    # return render_template("index.html", digits=tt, next_page=page+1)

@app.route("/")
def home():
    return render_template("index_demo.html")

@app.route("/post/<which_page>")
def post_one(which_page):

    data = db.session.query(ArticleForm.title, ArticleForm.post_time, ArticleForm.post_author,
                            ArticleContentForm.tmp_content, ArticleForm.views, ArticleForm.bg_img, ArticleForm.short_summary,
                            UserForm.username
                            ).join(ArticleContentForm, ArticleContentForm.md5_id == ArticleForm.md5_id
                                   ).join(
                                UserForm, UserForm.id == ArticleForm.post_author
                            ).filter(ArticleForm.md5_id == which_page).first()

    user_ip = re.sub("\.", "", request.remote_addr) or 0
    # print("sadd", READ_COUNT % which_page, int(user_ip))
    # client.sadd(READ_COUNT % which_page, int(user_ip))
    if len(data) == 0:
        return redirect("/post.html")
    if data[3] == "#" or True:
        try:
            fp = open("/home/zhangzhanming/flask/webapps/blog/document/%s.md" % "supervisor", encoding="utf8")
            text = fp.read()
            fp.close()
        except:
            traceback.print_exc()
            text = "# NOT FOUND"
    else:
        text = data[3]
    datajson = {
        "title":data[0],
        "post_time":data[1].strftime("%A %b %d, %Y"),
        "post_author":data[7],
        "content":Markup(markdown(text)),
        "bg_img":data[5],
        "views":data[4],
        "short_summary":data[6]
    }
    return render_template("post.html", digits=datajson)

@app.route("/<which_web_page>")
def redict_url(which_web_page):
    db.session.add(UserIpRecord(user_ip=request.remote_addr,
                                user_visit_time=datetime.now(),
                                visit_router=request.url))
    db.session.commit()
    if which_web_page == "index.html" or which_web_page == "post.html":
        return redirect("/")
    return render_template(which_web_page)



@app.route("/mail/contact_me.php", methods=['POST'])
def mail():
    formdata = request.form
    print(formdata)
    sendmail(name=formdata['name'], msg=formdata['message'], mail=formdata['mail'])
    return jsonify({"succ":1,"hh":2})


@app.route("/ss", methods=['GET'])
def search():
    db.session.add(UserIpRecord(user_ip=request.remote_addr,
                                user_visit_time=datetime.now(),
                                visit_router=request.url))
    db.session.commit()
    k = "%{}%".format(request.args.get("q"))
    fields = or_(ArticleForm.tags.like(k), ArticleForm.title.like(k), ArticleForm.short_summary.like(k))
    t = db.session.query(ArticleForm).filter(
        and_(ArticleForm.is_deleted == 0, fields)
    ).order_by(desc(ArticleForm.is_priority), desc(ArticleForm.post_time)
               ).all()
    tt = []
    for _ in t:
        author = db.session.query(UserForm.username).filter(UserForm.id == _.post_author).first()
        tmp = _.to_json()
        tmp['post_author'] = author[0] if author else ''
        tmp['post_time'] = tmp['post_time'].strftime("%Y-%m-%d %H:%M:%S")
        tt.append(tmp)
    return jsonify(tt)

@app.route("/s", methods=['GET'])
def searchS():
    k = request.args.get("q")
    data = spider.get_news(k)
    return jsonify(data)


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


