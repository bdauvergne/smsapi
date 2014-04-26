import logging
import requests

log = logging.getLogger(__name__)

URL = 'https://www.ovh.com/cgi-bin/sms/http2sms.cgi'
SMS_CLASS = 1

def is_int_phone_number(phone_number):
    if not phone_number.startswith('+'):
        return False
    if not phone_number[1:].isdigit():
        return False
    return True

class OVHError(object):
    pass

class OVH(object):
    def __init__(self, account, login, password, sms_from='', url=URL,
            sms_class=SMS_CLASS, no_stop=None, tag=None, deferred=None):
        self.url = url
        self.sms_class = sms_class
        self.account = account
        self.login = login
        self.password = password
        self.sms_from = sms_from
        self.no_stop = no_stop
        self.deferred = deferred
        self.tag = tag

    def send_sms(self, to, message, sms_class=None):
        sms_class = sms_class or self.sms_class
        message = unicode(message).encode('utf-8')
        to = list(to)
        if not all(map(is_int_phone_number, to)):
            raise ValueError('to must a list of phone '
                    'number using the international format')
        params = {
          'account': self.account,
          'login': self.login,
          'password': self.password,
          'from': self.sms_from,
          'to': to,
          'message': message,
          'contentType': 'text/json',
          'class': sms_class,
        }
        if self.no_stop:
            params['noStop'] = 1
        if self.tag:
            params['tag'] = self.tag[:20]
        if self.deferred:
            params['deferred'] = self.deferred.strftime('%H%M%d%m%Y')
        response = requests.get(self.url, params=params)
        result = response.json()
        status = result['status']
        if status >= 200:
            if status == 201:
                raise OVHError('missing parameter', result)
            if status == 202:
                raise OVHError('invalid parameter', result)
            if status == 401:
                raise OVHError('ip not authorized', result)
            raise OVHError('unknown error', result)
        return result
