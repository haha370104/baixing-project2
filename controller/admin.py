from flask import render_template, Blueprint, request, make_response, session, redirect, url_for
from model.model import *
from tools.security import *

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login/')
def login():
    pass


@admin_bp.route('/check_login/', methods=['GET', 'POST'])
def check_login():
    login_name = request.values.get('login_name')
    if login_name.find('@') != -1:
        staff = user.query.filter_by(email=login_name).first()
        if staff != None and staff.check_pwd(request.values.get('password')):
            token = get_salt(16)
            staff.token = token
            db.session.commit()
            res = make_response(redirect(url_for('admin.index')))
            res.set_cookie('token', user.token, expires=time.time() + 24 * 60 * 60)
            session['token'] = user.token
            return res
        else:
            return False
    else:
        staff = user.query.filter_by(phone=login_name).first()
        if staff != None and staff.check_pwd(request.values.get('password')):
            token = get_salt(16)
            staff.token = token
            db.session.commit()
            res = make_response(redirect(url_for('admin.index')))
            res.set_cookie('token', user.token, expires=time.time() + 24 * 60 * 60)
            session['token'] = user.token
            return True
        else:
            return False


@admin_bp.route('/index/')
def index():
    return render_template('admin/add_meeting.html')


@admin_bp.route('/get_staff/')
def get_staff():
    staffs = user.query.all()
    result = []
    for staff in staffs:
        result.append(staff.to_json())
    return json.dumps(result)
