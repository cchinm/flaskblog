from flask import Blueprint, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound
import hashlib

from module import SAVE_FILE_PATH

edit_page = Blueprint('edit_page', __name__, template_folder='templates')


@edit_page.route('/edit/create')
def create():
    """
    创建博文
    :return:
    """
    return render_template("post_edit.html")

@edit_page.route("/edit/publish", methods=['POST'])
def publish():
    """
    将博文发布
    :return:
    """
    try:
        formdata = request.form
        content = formdata['content']
        title = formdata['title']
        sn = hashlib.sha1(content.encode("utf8"))
        print(sn.hexdigest())
        with open(SAVE_FILE_PATH % title, "w") as f:
            f.write(content)
        return jsonify({"code":1, "data":"", "msg":"succ"})
    except Exception as e:
        return jsonify({"code":-1, "data":"", "msg":"%s" % e})


@edit_page.route("/edit/<id>")
def edit(id):
    """
    编辑，打开旧博文进行编辑
    :param id:
    :return:
    """
    try:
        with open(SAVE_FILE_PATH % id, "r", encoding="utf8", errors="ignore") as f:
            content = f.read()
        return render_template("post_edit.html", content=content)
    except Exception as e:
        print(e)
        return render_template("post_edit.html", content="打开失败")

@edit_page.route("/edit/list")
def edit_list():
    """
    打开博文列表
    :return:
    """
    tmp = ['tmp', 'paixu', 'heihei']
    return render_template('bse.html', list=tmp)

@edit_page.route("/edit/save")
def edit_save():
    """
    保存博文
    :return:
    """
    try:
        formdata = request.form
        content = formdata['content']
        title = formdata['title']
        sn = hashlib.sha1(content.encode("utf8"))
        print(sn.hexdigest())
        with open(SAVE_FILE_PATH % title, "w") as f:
            f.write(content)
        return jsonify({"code":1, "data":"", "msg":"succ"})
    except Exception as e:
        return jsonify({"code":-1, "data":"", "msg":"%s" % e})