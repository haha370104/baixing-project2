from app_config import db

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
    pay_time = db.Column(db.DateTime, nullable=False)


class meeting(Base):
    __tablename__ = 'meeting'

    ID = db.Column(db.Integer, primary_key=True)
    routing_flag = db.Column(db.Boolean, nullable=False, default=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    pun_rule = db.Column(db.Numeric(5, 2), nullable=False)
    pun_type = db.Column(db.Integer, nullable=False, default=0)
    pun_config = db.Column(db.String(300))


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
