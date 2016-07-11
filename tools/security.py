import random
import string
import hashlib


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
    sign = hashlib.sha1(tmp).hexdigest()
    if sign == signature:
        return True
    else:
        return False
