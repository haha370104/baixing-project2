from flask import Blueprint, render_template, request

wechat_bp = Blueprint('wechat', __name__)


@wechat_bp.route('/wechat_server/')
def wechat_server():
    print(request.url)
    return request.url
