from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from secret_config import db_url,port

app = Flask(__name__)

app.jinja_env.variable_start_string = '%%'
app.jinja_env.variable_end_string = '%%'
app.secret_key = 'A0Zr98jnjj/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://账号:密码@url:端口/数据库名'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ALLOW_FILE'] = ['jpg', 'jpeg', 'gif', 'png', 'bmp']
db = SQLAlchemy(app)
