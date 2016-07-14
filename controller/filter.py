from controller import *
from tools.wechat_tools import wechat_tools
from model.model import *
from flask import redirect, url_for


def wechat_check_access(request, session):
    if request.values.get('code'):
        return None
    else:
        if request.values.get('open_ID') or request.values.get('openid'):
            return None
    return '请从微信访问页面'


def wechat_check_register(request, session):
    open_ID = None
    if 'code' in request.values.keys():
        open_ID = wechat_tools.get_openID_by_code(request.values.get('code'))
        session['open_ID'] = open_ID
    if 'open_ID' in request.values.keys():
        open_ID = request.values.get('open_ID')
    elif 'openid' in request.values.keys():
        open_ID = request.values.get('openid')
    staff = user.query.filter(user.wechat_ID == open_ID).first()
    if staff != None:
        return None
    else:
        return redirect(url_for('wechat.register'))


def admin_check_login(request, session):
    token = request.cookies.get('token')
    if token == None:
        return redirect(url_for('admin.login'))
    if session.get('user_ID') == None:
        staff = user.query.filter(user.token == token).first()
        if staff == None:
            return redirect(url_for('admin.login'))
        else:
            session['user_ID'] = staff.ID
            return None
    else:
        return None


filter_list = {
    '/admin/set_session/': [admin_check_login],
    '/admin/index/': [admin_check_login],
    '/admin/get_meeting_list/': [admin_check_login],
    '/admin/get_fine_list/': [admin_check_login],
    '/admin/get_expenses_list/': [admin_check_login],
    '/admin/get_today_list/': [admin_check_login],
    '/admin/check_add_meeting/': [admin_check_login],
    '/admin/add_meeting/': [admin_check_login],
    '/wechat/register/': [wechat_check_access],
    '/wechat/check_register/': [wechat_check_access],
    '/wechat/get_fine/': [wechat_check_access, wechat_check_register],
    '/wechat/show_fine/': [wechat_check_access, wechat_check_register],
    '/wechat/show_fine_list/': [wechat_check_access, wechat_check_register],
    '/wechat/confirm_fine/': [wechat_check_access, wechat_check_register],
    '/wechat/spend_money/': [wechat_check_access, wechat_check_register],
    '/wechat/check_expense/': [wechat_check_access, wechat_check_register]
}
