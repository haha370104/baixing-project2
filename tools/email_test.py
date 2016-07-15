from model.model import *
import datetime

today = datetime.datetime.now().date()
today_fines = fine.query.filter(fine.happen_time.like(today.strftime('%Y-%m-%d') + '%')).all()

