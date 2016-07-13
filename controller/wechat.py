from flask import render_template, request, Blueprint
import xmltodict
from model.model import *
from tools.wechat_tools import *
from tools.security import *
from sqlalchemy import and_, or_, not_

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
                print(minutes)
                amount = 0
                if meet.pun_type == 0:
                    amount = float(meet.pun_rule) * max(minutes, 1)
                elif meet.pun_type == 1:
                    amount = float(meet.pun_rule)
                else:
                    pass  # TODO
                xml = wechat_tools.get_reply_xml(json['xml']['FromUserName'], json['xml']['ToUserName'],
                                                 '大兄弟快交钱,{0}元'.format(str(amount)))

                f = fine(staff.ID, meet.ID, amount)
                history = signin_history(staff.ID, meet.ID, True)
                db.session.add(history)
                db.session.add(f)
                db.session.commit()
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
                if dic['xml']['Event'] == 'SCAN':
                    xml = handle_scan(dic, request.values.get('openid'))
                    print(xml)
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
    return render_template('weui.html', open_ID=open_ID)


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
    return render_template('show.html')


@wechat_bp.route('/')
def ind():
    return '121231231233'
