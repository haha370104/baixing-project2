from app_config import app, port
from controller import blue_prints
from model.model import *
from sqlalchemy import and_, or_
import datetime
from flask import render_template

for bp in blue_prints:
    app.register_blueprint(bp[0], url_prefix=bp[1])


@app.route('/')
@app.route('/index/')
def index():
    return 'helloworld'


@app.route('/get_meeting_list/')
def get_meeting_list():
    now = datetime.datetime.now()
    n = datetime.datetime(1900, 1, 1, now.hour, now.minute, now.second)
    ms = meeting.query.filter(
        or_(and_(meeting.routing_flag, meeting.start_time > n), meeting.start_time > now)).all()
    result = []
    for m in ms:
        result.append(m.to_json())
    return json.dumps(result)


@app.route('/show_meeting/')
def show_meeting():
    return render_template('assembly.html')


@app.route('/get_QR_image/<int:meeting_ID>/')
def get_meeting_QR(meeting_ID):
    m = meeting.query.get(meeting_ID)
    ticket = m.get_ticket()
    return '<img src="{0}">'.format(get_QR_url(ticket))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
