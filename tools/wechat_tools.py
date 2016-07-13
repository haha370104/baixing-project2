import requests
import json
from secret_config import appid, appsecret
import time

token = 'ln_7JSFwckYcgExMHrwgGHGAMc4JMKsjiaZlxD99qSTiO5qHddKz7ozryaw1a8d2Jmz_bj7fRmsokhouW1QjmHBhxpx83lKbQGHgAxgfqEHCNdbH8CedEEJHV2F738EYWQTcAEAKEH'


class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def get_ticket(second, scene_id):
    r = requests.post('https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={0}'.format(token), data=json.dumps(
        {"expire_seconds": second, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}))
    j = json.loads(r.text)
    if 'ticket' in j.keys():
        return j['ticket']
    else:
        raise MyError('创建ticket出错')


def check_ticket(ticket):
    if ticket == None:
        return False
    r = requests.get(get_QR_url(ticket))
    if r.status_code == 200:
        return True
    else:
        return False


def get_openID_by_code(code):
    r = requests.get(
        'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'.format(
            appid, appsecret, code))
    j = json.loads(r.text)
    open_ID = j.get('openid')
    return open_ID


def get_QR_url(ticket):
    return 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=' + ticket


def get_reply_xml(open_ID, dev_user, content):
    xml = '''
        <xml>
            <ToUserName><![CDATA[{0}]]></ToUserName>
            <FromUserName><![CDATA[{1}]]></FromUserName>
            <CreateTime>{2}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{3}]]></Content>
        </xml>
    '''.format(open_ID, dev_user, str(int(time.time())), content)
    return xml
