import random
import string
import hashlib
import re


def get_salt(num):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, num))
    return salt


def get_cap_code():
    code = str(random.randint(0, 9999))
    zero_length = 4 - len(code)
    return '0' * zero_length + code


def check_signature(token, time, nonce, signature):
    tmp_arr = [token, time, nonce]
    tmp_arr.sort()
    tmp = ''.join(tmp_arr)
    sign = hashlib.sha1(tmp.encode()).hexdigest()
    if sign == signature:
        return True
    else:
        return False


def md5(s):
    return hashlib.md5(s.encode('ascii')).hexdigest()


def check_phone_num(s):
    def phonecheck(s):
        phoneprefix = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '150', '151', '152', '153',
                       '156', '158', '159', '170', '183', '182', '185', '186', '188', '189']
        if len(s) != 11:
            return False
        else:
            if s.isdigit():
                if s[:3] in phoneprefix:
                    return True
                else:
                    return False
            else:
                return False


def check_email_address(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False
