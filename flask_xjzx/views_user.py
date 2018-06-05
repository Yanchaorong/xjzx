from datetime import datetime
from flask import Blueprint, jsonify
from flask import current_app
from flask import make_response
from flask import redirect
from flask import request
from flask import session
import random
import re
from models import db, UserInfo, NewsInfo, NewsCategory
from flask import render_template
import functools
from utills.captcha.captcha import captcha

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


@user_blueprint.route('/image_yzm')
def image_yzm():
    name, yzm, image = captcha.generate_captcha()
    # yzm 表示随机生成验证码图片
    # 将数据保存
    session['image_yzm'] = yzm
    response = make_response(image)
    # 默认浏览器讲数据作为text/html解析
    # 需要告诉浏览器当前数据的类型为image/png
    response.mimetype = 'image/png'
    return response


@user_blueprint.route('/sms_yzm')
def sms_yzm():
    # 接收数据：手机号，图片验证码
    dect2 = request.args
    mobile = dect2.get('mobile')
    yzm = dect2.get('yzm')

    # 对比图片验证码
    if yzm != session['image_yzm']:
        return jsonify(result=1)

    # 随机生成一个4位的验证码
    yzm2 = random.randint(1000, 9999)

    # 将短信验证码进行保存，用于验证
    session['sms_yzm'] = yzm2
    print(session['sms_yzm'])
    # 发送短信
    from utills.ytx_sdk.ytx_send import sendTemplateSMS
    # sendTemplateSMS(mobile,{yzm2,5},1)
    print(yzm2)
    return jsonify(result=2)


@user_blueprint.route('/register', methods=['POST'])
def register():
    # 接收数据
    dect1 = request.form
    mobile = dect1.get('mobile')
    yzm_image = dect1.get('yzm_image')
    yzm_sms = dect1.get('yzm_sms')
    pwd = dect1.get('pwd')
    print(dect1)
    # 验证数据的有效性
    if not all([mobile, yzm_image, yzm_sms, pwd]):
        return jsonify(result=1)
        # 对比图片验证码
    if yzm_image != session['image_yzm']:
        return jsonify(result=2)
    # 对比短信验证码
    if int(yzm_sms) != session['sms_yzm']:
        return jsonify(result=3)
    # 判断密码长度
    if not re.match(r'[a-zA-Z0-9 + - * /]{6,16}', pwd):
        return jsonify(result=4)
    # 验证mobile是否纯在
    mobile_count = UserInfo.query.filter_by(mobile=mobile).count()
    if mobile_count > 0:
        return jsonify(result=5)
    # 创建对象
    user = UserInfo()
    user.nick_name = mobile
    user.mobile = mobile
    user.password = pwd
    # 提交到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except:
        current_app.logger_xjzx.error('用户注册访问数据库失败')
        return jsonify(result=6)

    return jsonify(result=7)


@user_blueprint.route('/login', methods=['POST'])
def login():
    dict1 = request.form
    mobile = dict1.get('mobile')
    pwd = dict1.get('pwd')
    # 验证有效性
    if not all([mobile, pwd]):
        return jsonify(result=1)
    # 查询判断，相应
    user = UserInfo.query.filter_by(mobile=mobile).first()

    if user:
        # 进行密码对比，flask内部提供了密码加密，对比的函数
        if user.check_pwd(pwd):
            session['user_id'] = user.id
            return jsonify(result=2, avatar=user.avatar, nick_name=user.nick_name)
        else:
            # 密码错误
            return jsonify(result=3)
    else:
        # 如果查询不到数据返回None,表示mobile错误
        return jsonify(result=4)


@user_blueprint.route('/logout', methods=['POST'])
def logout():
    del session['user_id']
    return jsonify(result=1)


# 测试用
@user_blueprint.route('/sessio')
def sessio():
    session['a'] = 10
    if 'user_id' in session:
        print(session['user_id'])
        return 'ok'
    else:
        return 'no'


def fun(views):
    @functools.wraps(views)
    def fun2(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/')
        return views(*args, **kwargs)

    return fun2


@user_blueprint.route('/')
@fun
def index():
    user_id = session['user_id']
    user = UserInfo.query.get(user_id)
    return render_template('news/user.html', user=user)


@user_blueprint.route('/base', methods=['GET', 'POST'])
@fun
def base():
    user_id = session['user_id']
    user = UserInfo.query.get(user_id)
    if request.method == 'GET':
        return render_template('news/user_base_info.html', user=user)
    elif request.method == 'POST':
        dict1 = request.form
        signature = dict1.get('signature')
        nick_name = dict1.get('nick_name')
        gender = dict1.get('gender')
        if gender == 'True':
            gender = True
        else:
            gender = False
        user.signature = signature
        user.nick_name = nick_name
        user.gender = gender
        db.session.commit()
        return jsonify(result=1)


#
@user_blueprint.route('/pic', methods=['GET', 'POST'])
@fun
def pic():
    user_id = session['user_id']
    user = UserInfo.query.get(user_id)
    if request.method == 'GET':
        return render_template('news/user_pic_info.html', user=user)
    elif request.method == 'POST':
        dict1 = request.form
        avatar = dict1.get('avatar')
        user.avatar = avatar
        str1 = user.avatar
        use = re.split(r"\\", str1)
        user.avatar = use[2]
        db.session.commit()
        return jsonify(result=1, avater=use)


@user_blueprint.route('/follow')
@fun
def follow():
    user_id = session['user_id']
    user = UserInfo.query.get(user_id)
    # 获取当前页码值
    page = int(request.args.get('page', '1'))
    # 通过关联属性获取关注的用户对象
    # 对查询的数据进行分页

    pagination = user.follow_user.paginate(page, 4, False)
    user_list = pagination.items
    total_page = pagination.pages
    return render_template('news/user_follow.html', user_list=user_list, total_page=total_page, page=page)


@user_blueprint.route('/pword', methods=['GET', 'POST'])
@fun
def pword():
    if request.method == 'GET':
        return render_template('news/user_pass_info.html')
    elif request.method == 'POST':
        dict1 = request.form
        oldpwd = dict1.get('oldpwd')
        newpwd = dict1.get('newpwd')
        newpwd2 = dict1.get('newpwd2')
        if not all([oldpwd, newpwd, newpwd2]):
            return render_template('news/user_pass_info.html', msg='请输入密码')
        if not re.match(r'[a-zA-Z0-9_]{6,16}', newpwd):
            return render_template('news/user_pass_info.html', msg='密码格式错误，只能是字母、数字、符号')
        if newpwd != newpwd2:
            return render_template('news/user_pass_info.html', msg='两次密码不一致')
        user = UserInfo.query.get(session['user_id'])
        print(oldpwd)
        if not user.check_pwd(oldpwd):
            return render_template('news/user_pass_info.html', msg='当前密码错误', oldpwd=oldpwd, newpwd=newpwd,
                                   newpwd2=newpwd2)
        user.password = newpwd
        db.session.commit()
        return render_template('news/user_pass_info.html', msg='修改成功')


@user_blueprint.route('/collection')
@fun
def collection():
    user_id = session['user_id']
    user = UserInfo.query.get(user_id)
    # 获取当前页码值
    page = int(request.args.get('page', '1'))
    # 通过关联属性获取关注用户对象
    pagination = user.news_collect.paginate(page, 6, False)
    user_list = pagination.items
    total_page = pagination.pages
    return render_template('news/user_collection.html', user_list=user_list, total_page=total_page, page=page)


@user_blueprint.route('/release', methods=['GET', 'POST'])
@fun
def release():
    # 查询新闻分类
    #
    category = NewsCategory.query.all()
    if request.method == 'GET':
        return render_template('news/user_news_release.html', category=category)
    elif request.method == 'POST':
        dict1 = request.form
        title = dict1.get('title')
        category_id = dict1.get('category_id')
        summary = dict1.get('summary')
        content = dict1.get('content')
        pic = dict1.get('pic')
        print(dict1)
        if not all([title, category_id, summary, content, pic]):
            print(111)
            return jsonify(result=1, title=title, category_id=category_id, summary=summary, content=content, pic=pic)
        # p=pic
        # str1=p
        # us=re.split(r'\\',str1)
        # print(us)
        news = NewsInfo()
        print(news)
        news.category_id = category_id
        news.pic = pic
        str1 = news.pic
        use = re.split(r"\\", str1)
        print(use[2])
        news.pic= use[2]
        news.title = title
        news.summary = summary
        news.content = content
        news.user_id = session['user_id']
        db.session.add(news)
        db.session.commit()
        return jsonify(result=2)


@user_blueprint.route('/newslist')
@fun
def newslist():
    user_id = session['user_id']
    user = UserInfo.query.get(user_id)
    page = int(request.args.get('page', '1'))
    # 通过关联属性获取用户对象
    pagination = user.news.order_by(NewsInfo.update_time.desc()).paginate(page,6,False)

    news_list = pagination.items
    total_page = pagination.pages

    return render_template('news/user_news_list.html', user=user,news_list=news_list,page=page, total_page=total_page)

@user_blueprint.route('/release_updata/<int:news_id>',methods=['GET','POST'])
def release_updata(news_id):
    news = NewsInfo.query.get(news_id)
    category=NewsCategory.query.all()
    if request.method == 'GET':
        return render_template('news/user_news_release_updata.html', category=category,news=news)
    elif request.method == 'POST':
        dict1 = request.form
        title = dict1.get('title')
        category_id = dict1.get('category_id')
        summary = dict1.get('summary')
        content = dict1.get('content')
        # pic = request.files.get('news_pic')
        if not all([title, category_id, summary, content]):
            return render_template('news/user_news_release.html',category=category,news=news)
        # p=pic
        # str1=p
        # us=re.split(r'\\',str1)
        # print(us)
        news.category_id = category_id
        # news.pic = pic
        # str1 = news.pic
        # use = re.split(r"\\", str1)
        # news.pic = use[2]
        news.title = title
        news.summary = summary
        news.content = content
        news.user_id = session['user_id']
        news.updata_time= datetime.now()
        news.status=1
        db.session.commit()
        print('111')
        return redirect('/user/newslist')














