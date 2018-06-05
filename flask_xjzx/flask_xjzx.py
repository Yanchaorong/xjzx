from flask_script import Manager

from app import create_app
from config import DevelopConfig

app = create_app(DevelopConfig)

manager = Manager(app)

from models import db
# 初始化数据库
db.init_app(app)
#
from flask_migrate import Migrate, MigrateCommand
# 自定义命令用于数据库迁移
Migrate(app, db)
manager.add_command('bbb', MigrateCommand)

if __name__ == '__main__':
    #manager.run()
    app.run(port=8000)
