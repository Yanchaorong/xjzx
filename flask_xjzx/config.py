import redis
import os


class Config(object):
    # 数据库配置
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/xjzx'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # redis配置
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 10
    # session
    SECRET_KEY = "zhuqi"
    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)  # 使用 redis 的实例
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 14  # session 的有效期，单位是秒

    # 表示项目的根目录
    # __file__==>当前文件名config.py
    # os.path.abspath()==>获取文件的绝对路径，/home/python/Desktop/sz10_flask/xjzx/config.py
    # os.path.dirname()==>获取路径的目录名，/home/python/Desktop/sz10_flask/xjzx
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DevelopConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/xjzx'
