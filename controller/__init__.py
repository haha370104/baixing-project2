from controller.wechat import wechat_bp
from controller.admin import admin_bp

blue_prints = []
blue_prints.append([wechat_bp, '/wechat'])
blue_prints.append([admin_bp, '/admin'])
