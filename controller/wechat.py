from flask import Blueprint, render_template, request
from tools.security import *

wechat_bp = Blueprint('wechat', __name__)


@wechat_bp.route('/wechat_server/')
def wechat_server():
    print(request.url)
    if check_signature('token', request.args.get('timestamp'), request.args.get('nonce'),
                       request.args.get('signature')):
        return request.args.get('echostr')
    else:
        return request.url
