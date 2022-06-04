from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'  # 设置数据库路径
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 解决某个奇妙的报错
db = SQLAlchemy(app)

from diary import routes

db.create_all()