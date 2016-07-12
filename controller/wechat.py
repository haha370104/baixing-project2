from flask import Blueprint, render_template, request
from tools.security import *
import xmltodict

wechat_bp = Blueprint('wechat', __name__)


@wechat_bp.route('/wechat_server/', methods=['GET', 'POST'])
def wechat_server():
    if check_signature('token', request.args.get('timestamp'), request.args.get('nonce'),
                       request.args.get('signature')):
        if 'ehcostr' in request.args:
            return request.args.get('ehcostr')
        else:
            print(request.data)
            return 'success'
    else:
        return request.url
