from flask import render_template, Blueprint, request, make_response, session, redirect, url_for
from model.model import *
from tools.security import *
from controller.filter import *

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
def admin_filter():
    path = request.path
    if path in filter_list.keys():
        for fun in filter_list[path]:
            response = fun(request, session)
            if response != None:
                return response
        return None
    return None


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


@admin_bp.route('/set_session/')
def set_session():
    token = request.cookies.get('token')
    staff = user.query.filter(user.token == token).first()
    session['user_ID'] = staff.ID
    url = request.values.get('url')
    return redirect(url)


@admin_bp.route('/index/')
def index():
    staff = user.query.get(session.get('user_ID'))
    return render_template('admin/index.html', amount=float(staff.money))


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


@admin_bp.route('/get_today_list/')
def get_today_list():
    today = datetime.datetime.now().date()
    ond_day = datetime.timedelta(days=1)
    tomorrow = today + ond_day
    expenes = expenses.query.filter(and_(today < expenses.occur_time, tomorrow > expenses.occur_time)).all()
    result = []
    for expen in expenes:
        result.append(expen.to_json_with_username())
    return json.dumps(result)


@admin_bp.route('/add_meeting/')
def add_meeting():
    return render_template('admin/add_meeting.html')


@admin_bp.route('/check_add_meeting/', methods=['POST', 'GET'])
def check_add_meeting():
    meeting_topic = request.values.get('meeting_name')
    routing_flag = request.values.get('meeting_type') == "1"
    if routing_flag:
        start_time = datetime.datetime.strptime(request.values.get('start_time'), "%H:%M")
        end_time = datetime.datetime.strptime(request.values.get('end_time'), "%H:%M")
    else:
        meeting_date = request.values.get('meeting_date')
        start_time = datetime.datetime.strptime(meeting_date + ' ' + request.values.get('start_time'), "%Y-%m-%d %H:%M")
        end_time = datetime.datetime.strptime(meeting_date + ' ' + request.values.get('end_time'), "%Y-%m-%d %H:%M")
    pun_type = int(request.values.get('punish_type'))
    pun_rule = request.values.get('fixed_money' + str(pun_type))
    if pun_rule != '':
        pun_rule = float(pun_rule)
    pun_config = request.values.get('self_design')
    if pun_config.find('import') != -1:
        return '''
        <script>
            alert('西方的哪一个国家我没去过,不import够你用');
            history.back();
        </script>
        '''
    meet = meeting(routing_flag, start_time, end_time, pun_rule, pun_type, meeting_topic, pun_config)
    db.session.add(meet)
    db.session.commit()
    return redirect(url_for('admin.index'))
