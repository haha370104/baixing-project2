from app_config import db
from tools.wechat_tools import *
from tools.security import *
import datetime

Base = db.Model


class ask_leave(Base):
    __tablename__ = 'ask_leave'
    __table_args__ = (
        db.Index('user_ID', 'user_ID', 'meeting_ID', 'effective_time', unique=True),
    )

    ID = db.Column(db.Integer, primary_key=True)
    user_ID = db.Column(db.Integer, nullable=False)
    meeting_ID = db.Column(db.Integer, nullable=False)
    apply_time = db.Column(db.DateTime, nullable=False)
    effective_time = db.Column(db.Date, nullable=False)


class expense(Base):
    __tablename__ = 'expenses'

    ID = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.DECIMAL(6, 2), nullable=False)
    occur_time = db.Column(db.DateTime, nullable=False)
    remark = db.Column(db.String(300))


class fine(Base):
    __tablename__ = 'fine'

    ID = db.Column(db.Integer, primary_key=True)
    user_ID = db.Column(db.Integer, nullable=False, index=True)
    meeting_ID = db.Column(db.Integer, nullable=False, index=True)
    amount = db.Column(db.DECIMAL(5, 2), nullable=False)
    happen_time = db.Column(db.DateTime, nullable=False)
    pay_flag = db.Column(db.Boolean, nullable=False)
    pay_time = db.Column(db.DateTime)

    def __init__(self, user_ID, meeting_ID, amount):
        self.user_ID = user_ID
        self.meeting_ID = meeting_ID
        self.amount = amount
        self.happen_time = datetime.datetime.now()
        self.pay_flag = False

    def to_json(self):
        dic = {}
        dic['ID'] = self.ID
        dic['meeting_ID'] = self.meeting_ID
        dic['amount'] = float(self.amount)
        dic['happen_time'] = str(self.happen_time)
        return dic

    def wechat_ajax(self):
        dic = {}
        dic['ID'] = self.ID
        dic['text'] = str(self.happen_time) + '的会议中迟到,罚款' + str(float(self.amount)) + '元'
        dic['pay_flag'] = self.pay_flag
        return dic

    def check(self):
        self.pay_flag = True
        self.pay_time = datetime.datetime.now()


class meeting(Base):
    __tablename__ = 'meeting'

    ID = db.Column(db.Integer, primary_key=True)
    routing_flag = db.Column(db.Boolean, nullable=False, default=False)
    start_time = db.Column('start_time', db.DateTime, nullable=False)
    end_time = db.Column('end_time', db.DateTime, nullable=False)
    pun_rule = db.Column(db.Numeric(5, 2), nullable=False)
    pun_type = db.Column(db.Integer, nullable=False, default=0)
    pun_config = db.Column(db.String(300))
    ticket = db.Column(db.String(100))
    screen_ID = db.Column(db.Integer, unique=True)

    def __init__(self, routing_flag, start_time, end_time, pun_rule, pun_type, pun_config=None):
        self.routing_flag = routing_flag
        if routing_flag:
            self.start_time = datetime.datetime(1900, 1, 1, start_time.hour, start_time.minute, start_time.second)
            self.end_time = datetime.datetime(1900, 1, 1, end_time.hour, end_time.minute, end_time.second)
        else:
            self.start_time = start_time
            self.end_time = end_time
        self.pun_rule = pun_rule
        self.pun_type = pun_type
        self.pun_config = pun_config

    def check_legal(self):
        if self.routing_flag:
            end = self.get_end_time()
            now = datetime.datetime.now().time()
            return end >= now
        else:
            now = datetime.datetime.now()
            return self.end_time >= now
        pass

    def get_ticket(self):
        if self.screen_ID == None:
            self.screen_ID = self.ID + 10000
        if wechat_tools.check_ticket(self.ticket):
            return self.ticket
        else:
            start = datetime.datetime.now()
            end = self.end_time.timetuple()
            seconds = (end.tm_hour - start.hour) * 3600 + (end.tm_min - start.minute) * 60 + (
                end.tm_sec - start.second)
            self.ticket = wechat_tools.get_ticket(seconds, self.screen_ID)  # 需要调试
            db.session.commit()
            return self.ticket

    def to_json(self):
        dic = {}
        dic['ID'] = self.ID
        dic['routing_flag'] = self.routing_flag
        dic['start_time'] = str(self.start_time)
        dic['end_time'] = str(self.end_time)
        dic['pun_rule'] = str(float(self.pun_rule))
        dic['pun_type'] = self.pun_type
        dic['pun_config'] = self.pun_config
        dic['ticket'] = self.get_ticket()
        dic['screen_ID'] = self.screen_ID
        if self.routing_flag:
            start_time = dic['start_time'].split(' ')[1]
            end_time = dic['end_time'].split(' ')[1]
            dic['text'] = '常规会议\n开始时间:{0}\n,结束时间:{1}'.format(start_time, end_time)
        else:
            dic['text'] = '非常规会议\n开始时间:{0}\n,结束时间:{1}'.format(dic['start_time'], dic['end_time'])
        return dic

    def get_start_time(self):
        start_time = str(self.start_time).split(' ')[1]
        start_time = datetime.datetime.strptime(start_time, '%H:%M:%S').time()
        return start_time

    def get_end_time(self):
        end_time = str(self.end_time).split(' ')[1]
        end_time = datetime.datetime.strptime(end_time, '%H:%M:%S').time()
        return end_time


t_meeting_user = db.Table('t_meeting_user',
                          db.Column('user_ID', db.Integer, db.ForeignKey('meeting_ID.ID'), nullable=False),
                          db.Column('meeting_ID', db.Integer, db.ForeignKey('user_ID.ID'), nullable=False)
                          )


class money(Base):
    __tablename__ = 'money'

    ID = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.DECIMAL(7, 2), nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False)


class user(Base):
    __tablename__ = 'user'

    ID = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    wechat_ID = db.Column(db.String(200), nullable=False, unique=True)
    phone = db.Column(db.String(11), unique=True)
    salt = db.Column(db.String(16), nullable=False)
    passwd = db.Column(db.String(32), nullable=False)
    token = db.Column(db.String(16))

    def __init__(self, user_name, email, wechat_ID, phone, passwd):
        self.user_name = user_name
        self.email = email
        self.wechat_ID = wechat_ID
        self.phone = phone
        self.salt = get_salt(16)
        self.passwd = md5(passwd + self.salt)

    def check_pwd(self, passwd):
        if self.passwd == md5(passwd + self.salt):
            self.token = get_salt(16)
            db.session.commit()
            return True
        else:
            return False


class signin_history(Base):
    __tablename__ = 'signin_history'

    ID = db.Column(db.Integer, primary_key=True)
    sign_time = db.Column(db.Time, nullable=False)
    happen_date = db.Column(db.Date, nullable=False)
    user_ID = db.Column(db.Integer, nullable=False, index=True)
    meeting_ID = db.Column(db.Integer, nullable=False, index=True)
    late_flag = db.Column(db.Boolean, nullable=False)
    delete_flag = db.Column(db.Boolean, default=True)

    def __init__(self, user_ID, meeting_ID, late_flag):
        self.user_ID = user_ID
        self.meeting_ID = meeting_ID
        self.sign_time = datetime.datetime.now().time()
        self.happen_date = datetime.datetime.now().date()
        self.late_flag = late_flag

    def to_json(self):
        dic = {}
        dic['name'] = user.query.get(self.user_ID).user_name
        dic['flag'] = self.late_flag
        return dic

    def delete(self):
        self.delete_flag = False
