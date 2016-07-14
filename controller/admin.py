from flask import render_template, Blueprint, request, make_response, session, redirect, url_for
from model.model import *
from tools.security import *

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login/')
def login():
    return render_template('admin/login.html')


@admin_bp.route('/check_login/', methods=['GET', 'POST'])
def check_login():
    login_name = request.values.get('login_name')
    if login_name.find('@') != -1:
        staff = user.query.filter_by(email=login_name).first()
        if staff != None and staff.check_pwd(request.values.get('password')):
            res = make_response('<script>location.href="/admin/index/"</script>')
            res.set_cookie('token', staff.token, expires=time.time() + 24 * 60 * 60)
            session['user_ID'] = staff.ID
            session['token'] = staff.token
            return res
        else:
            return False
    else:
        staff = user.query.filter_by(phone=login_name).first()
        if staff != None and staff.check_pwd(request.values.get('password')):
            res = make_response('<script>location.href="/admin/index/"</script>')
            res.set_cookie('token', staff.token, expires=time.time() + 24 * 60 * 60)
            session['user_ID'] = staff.ID
            session['token'] = staff.token
            return res
        else:
            return False


@admin_bp.route('/index/')
def index():
    return render_template('admin/index.html')


@admin_bp.route('/get_meeting_list/')
def get_meeting_list():
    now = datetime.datetime.now()
    meetings = meeting.query.filter(
        or_(meeting.routing_flag == True, and_(meeting.routing_flag == False, meeting.end_time > now))).all()
    result = []
    for meet in meetings:
        result.append(meet.to_json())
    return json.dumps(result)


@admin_bp.route('/get_fine_list/')
def get_fine_list():
    user_ID = session.get('user_ID')
    fines = fine.query.filter(fine.user_ID == user_ID).all()
    result = []
    for f in fines:
        result.append(f.to_json())
    return json.dumps(result)


@admin_bp.route('/get_expenses_list/')
def get_expenses_list():
    user_ID = session.get('user_ID')
    expenes = expenses.query.filter(expenses.user_ID == user_ID).all()
    expenes.reverse()
    result = []
    for expen in expenes:
        result.append(expen.to_json())
    return json.dumps(result)
