from flask import Blueprint, render_template, request
from tools.security import *
import xmltodict
from tools.wechat_tools import *

wechat_bp = Blueprint('wechat', __name__)


@wechat_bp.route('/wechat_server/', methods=['GET', 'POST'])
def wechat_server():
    if check_signature('token', request.args.get('timestamp'), request.args.get('nonce'),
                       request.args.get('signature')):
        if 'echostr' in request.args:
            return request.args.get('echostr')
        else:
            print(request.data)
            # 处理逻辑都写在这里

            return 'success'
    else:
        return request.url


@wechat_bp.route('/QR_image/<string:ticket>/')
def QR_image(ticket):
    return '<img src="{0}">'.format(get_QR_image(ticket))


@wechat_bp.route('/')
def ind():
    return '121233'
