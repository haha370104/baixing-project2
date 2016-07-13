from flask import Blueprint, render_template, request
from tools.security import *
import xmltodict
from model.model import *
from tools.wechat_tools import *
from tools.security import *
from sqlalchemy import and_, or_, not_

wechat_bp = Blueprint('wechat', __name__)


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
                    ticket = dic['xml']['Ticket']
                    screen_ID = dic['xml']['EventKey']
                    wechat_ID = request.values.get('openid')
                    staff = user.query.filter_by(wechat_ID=wechat_ID).first()
                    meet = meeting.query.filter(and_(meeting.ticket == ticket, meeting.screen_ID == screen_ID)).first()
                    xml = None
                    if meet == None:
                        xml = get_reply_xml(dic['xml']['FromUserName'], dic['xml']['ToUserName'], '非法操作')
                    else:
                        start_time = meet.get_start_time()
                        now = datetime.datetime.now().time()
                        if start_time >= now:
                            print('没迟到')
                            xml = get_reply_xml(dic['xml']['FromUserName'], dic['xml']['ToUserName'], '恭喜你大兄弟,没迟到!')
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
                            print('需要交罚款', amount)
                            xml = get_reply_xml(dic['xml']['FromUserName'], dic['xml']['ToUserName'],
                                                '大兄弟快交钱,{0}元'.format(str(amount)))
                            f = fine(staff.ID, meet.ID, amount)
                            db.session.add(f)
                            db.session.commit()
                    # print(xml)
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
    open_ID = get_openID_by_code(code)
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
    open_ID = get_openID_by_code(code)
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
