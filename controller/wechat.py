from flask import render_template, request, Blueprint
import xmltodict
from model.model import *
from tools.wechat_tools import *
from tools.security import *
from sqlalchemy import and_, or_, not_
from tools.weather_tools import *

wechat_bp = Blueprint('wechat', __name__)


def handle_scan(json, wechat_ID):
    ticket = json['xml']['Ticket']
    screen_ID = json['xml']['EventKey']
    staff = user.query.filter_by(wechat_ID=wechat_ID).first()
    meet = meeting.query.filter(and_(meeting.ticket == ticket, meeting.screen_ID == screen_ID)).first()
    xml = None
    if meet == None:
        xml = wechat_tools.get_reply_xml(json['xml']['FromUserName'], json['xml']['ToUserName'], '非法操作')
    else:
        start_time = meet.get_start_time()
        now = datetime.datetime.now().time()
        history = signin_history.query.filter(and_(signin_history.meeting_ID == meet.ID,
                                                   signin_history.happen_date == datetime.datetime.now().date(),
                                                   signin_history.user_ID == staff.ID)).first()
        if history != None:
            xml = wechat_tools.get_reply_xml(json['xml']['FromUserName'], json['xml']['ToUserName'],
                                             '不要重复签到啊!')
        else:
            if start_time >= now:
                xml = wechat_tools.get_reply_xml(json['xml']['FromUserName'], json['xml']['ToUserName'],
                                                 '恭喜你大兄弟,没迟到!')
                history = signin_history(staff.ID, meet.ID, False)
                db.session.add(history)
                db.session.commit()
            else:
                minutes = (now.hour - start_time.hour) * 60 + (now.minute - start_time.minute)
                amount = 0
                if meet.pun_type == 0:
                    amount = float(meet.pun_rule) * max(minutes, 1)
                elif meet.pun_type == 1:
                    amount = float(meet.pun_rule)
                else:
                    amount = eval(meet.pun_config)  # TODO
                xml = wechat_tools.get_reply_xml(json['xml']['FromUserName'], json['xml']['ToUserName'],
                                                 '大兄弟快交钱,{0}元'.format(str(amount)))

                f = fine(staff.ID, meet.ID, amount)
                history = signin_history(staff.ID, meet.ID, True)
                db.session.add(history)
                db.session.add(f)
                db.session.commit()
    return xml


def handle_weather(json):
    weather_json = get_tomorrow_weather()
    reply_content = '明天温度{0},{1},风力为{2}'.format(weather_json['temperature'], weather_json['weather'],
                                                weather_json['wind'])
    xml = wechat_tools.get_reply_xml(json['xml']['FromUserName'], json['xml']['ToUserName'],
                                     reply_content)
    return xml


@wechat_bp.route('/wechat_server/', methods=['GET', 'POST'])
def wechat_server():
    if check_signature('token', request.args.get('timestamp'), request.args.get('nonce'),
                       request.args.get('signature')):
        if 'echostr' in request.args:
            return request.args.get('echostr')
        else:
            xml_data = request.data
            dic = xmltodict.parse(xml_data)
            print(json.dumps(dic))
            # 处理逻辑都写在这里
            try:
                # print(dic.get('xml').get('MsgType'))
                # print(dic.get('xml').get('Content'))
                if dic.get('xml').get('Event') == 'SCAN':
                    xml = handle_scan(dic, request.values.get('openid'))
                    print(xml)
                    return xml
                elif dic.get('xml').get('MsgType') == 'text' and dic.get('xml').get('Content').find('天气') > -1:
                    print('要天气')
                    xml = handle_weather(dic)
                    return xml
                else:
                    return 'success'
            except:
                return 'success'
    else:
        return request.url


@wechat_bp.route('/register/', methods=['GET', 'POST'])
def pre_register():
    code = request.values.get('code')
    open_ID = wechat_tools.get_openID_by_code(code)
    return render_template('wechat/register.html', open_ID=open_ID)


@wechat_bp.route('/check_register/', methods=['GET', 'POST'])
def check_register():
    phone = request.values.get('phone')
    email = request.values.get('email')
    username = request.values.get('username')
    password = request.values.get('password')
    open_ID = request.values.get('open_ID')
    staff = user(username, email, open_ID, phone, password)  # 需要获取openID
    db.session.add(staff)
    db.session.commit()
    return 'success'


@wechat_bp.route('/get_fine/')
def get_fines():
    code = request.values.get('code')
    open_ID = wechat_tools.get_openID_by_code(code)
    user_ID = user.query.filter(user.wechat_ID == open_ID).first().ID
    fs = fine.query.filter(and_(fine.user_ID == user_ID, not_(fine.pay_flag))).all()
    result = []
    for f in fs:
        result.append(f.wechat_ajax())
    return json.dumps(result)


@wechat_bp.route('/show_fine/')
def show_fine():
    return render_template('wechat/pun_show.html')


@wechat_bp.route('/show_fine_list/')
def show_fine_list():
    code = request.values.get('code')
    open_ID = wechat_tools.get_openID_by_code(code)
    staff = user.query.filter_by(wechat_ID=open_ID).first()
    puns = fine.query.filter(and_(fine.user_ID == staff.ID, not_(fine.pay_flag))).all()
    result = []
    for pun in puns:
        result.append(pun.wechat_ajax())
    return json.dumps(result)


@wechat_bp.route('/confirm_fine/', methods=['POST', 'GET'])
def confirm_fine():
    data = request.values.get('fine_list')
    fine_list = json.loads(data)
    for fine_ID in fine_list:
        f = fine.query.get(fine_ID)
        happen_date = f.happen_time.date()
        meeting_ID = f.meeting_ID
        historys = signin_history.query.filter(
            and_(signin_history.meeting_ID == meeting_ID, signin_history.happen_date == happen_date,
                 not_(signin_history.late_flag))).all()
        if len(historys) == 0:
            break
        per_amount = float(f.amount) / len(historys)
        for history in historys:
            staff = user.query.get(history.user_ID)
            staff.money = float(staff.money) + per_amount
        print(f.amount)
        f.check()
    db.session.commit()
    return '成功'


@wechat_bp.route('/')
def ind():
    return '121231231233'
