import requests
from app_config import app
import json
import time,datetime
from sqlalchemy import and_, or_


class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class wechat_tools():
    appid = app.config.get('app_id')
    appsecret = app.config.get('app_secret')
    token = app.config.get('wechat_token')

    @staticmethod
    def check_token():
        if wechat_tools.token == None:
            wechat_tools.get_token()
        r = requests.get('https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=' + wechat_tools.token)
        j = json.loads(r.text)
        if 'errcode' in j.keys():
            wechat_tools.get_token()
        return wechat_tools.token

    @staticmethod
    def get_token():
        r = requests.get(
            'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'.format(
                wechat_tools.appid, wechat_tools.appsecret))
        result = json.loads(r.text)
        wechat_tools.token = result['access_token']
        return wechat_tools.token

    @staticmethod
    def get_ticket(second, scene_id):
        r = requests.post(
            'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={0}'.format(wechat_tools.check_token()),
            data=json.dumps(
                {"expire_seconds": second, "action_name": "QR_SCENE",
                 "action_info": {"scene": {"scene_id": scene_id}}}))
        j = json.loads(r.text)
        if 'ticket' in j.keys():
            return j['ticket']
        else:
            raise MyError('创建ticket出错')

    @staticmethod
    def check_ticket(ticket):
        if ticket == None:
            return False
        r = requests.get(wechat_tools.get_QR_url(ticket))
        if r.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def get_openID_by_code(code):
        r = requests.get(
            'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'.format(
                wechat_tools.appid, wechat_tools.appsecret, code))
        j = json.loads(r.text)
        open_ID = j.get('openid')
        return open_ID

    @staticmethod
    def get_QR_url(ticket):
        return 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=' + ticket

    @staticmethod
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


