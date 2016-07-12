import requests
import json

token = 'kqxZN_SKyOmkqTvJlwauIxpYnZHzjAjr3uOaWFS1IqtbUmJQSThp8li-AfLuyxEfm3jyd9ZbDLSab04YakkuPvE4V3-ZH3bjKHw_Lj4lE8YSDGjAAANYB'


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


def get_QR_image(ticket):
    return 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=' + ticket
