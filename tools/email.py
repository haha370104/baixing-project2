import smtplib
from email.mime.text import MIMEText


class email:
    _user = ""
    _pwd = ""
    _to = ""
    _host = ''
    s = None

    def __init__(self, user, pwd, host):
        self._user = user
        self._pwd = pwd
        self._host = host
        self.s = smtplib.SMTP(self._host, port=587)
        self.s.ehlo()
        self.s.starttls()
        self.s.login(self._user, self._pwd)

    def send_email(self, to, title, content):
        msg = MIMEText(content)
        msg['Subject'] = title
        msg['TO'] = to
        msg['From'] = self._user
        self.s.sendmail(self._user, self._to, msg.as_string(()))

    def quit(self):
        self.s.close()


if __name__ == '__main__':
    e = email('luoxiangyu@baixing.com', 'ttkl1231+1s', 'smtp.partner.outlook.cn')
    e.send_email('haha370104@gmail.com', 'heiheihei', 'content')
