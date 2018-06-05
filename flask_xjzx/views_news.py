from flask import Blueprint,session, jsonify
from flask import request

from models import NewsInfo,NewsCategory,NewsComment,UserInfo,db
from flask import current_app
from flask import render_template

news_blueprint = Blueprint('news', __name__)

@news_blueprint.route('/')
def index():
    category=NewsCategory.query.all()
    if 'user_id' in session:
        user=UserInfo.query.get(session['user_id'])
    else:
        user = None
    count_list=NewsInfo.query.filter_by(status=2).order_by(NewsInfo.click_count.desc())[0:6]
    return render_template('news/index.html',category=category ,user=user,count_list=count_list)
@news_blueprint.route('/newslist')
def newslist():
    # 查询新闻数据==》
    # 接受请求的页码值
    page = int(request.args.get('page','1'))
    pagination= NewsInfo.query.filter_by(status=2)
    # 接收分类的编号
    category_id=int(request.args.get('category_id','0'))
    if category_id:
        pagination=NewsInfo.query.filter_by(category_id=category_id)
    # 排序,分页
    pagination = pagination.order_by(NewsInfo.update_time.desc()).paginate(page,4,False)
    # 获取当前页的数据
    news_list= pagination.items
    news_list2=[]
    for news in news_list:
        new_dict={
            'id':news.id,
            'pic':news.pic,
            'title':news.title,
            'summary':news.summary,
            'user_avater':news.user.avater_for,
            'user_nick_name':news.user.nick_name,
            'update':news.update_time.strftime('%Y-%m-%d'),
            'user_id':news.user.id,
            'category_id':news.category_id
        }
        news_list2.append(new_dict)
    return jsonify(news_list=news_list2)