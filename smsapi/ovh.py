import logging
import requests
import datetime

from . import utils

log = logging.getLogger(__name__)

URL = 'https://www.ovh.com/cgi-bin/sms/http2sms.cgi'
SMS_CLASS = 1

class OVH(object):
    def __init__(self, account, login, password, sms_from='', url=URL,
            sms_class=SMS_CLASS, no_stop=None, tag=None, deferred=None):
        assert deferred  is None or isinstance(deferred, datetime.datetime)
        self.url = url
        self.sms_class = sms_class
        self.account = account
        self.login = login
        self.password = password
        self.sms_from = sms_from
        self.no_stop = no_stop
        self.deferred = deferred
        self.tag = tag

    def send_sms(self, to, message, sms_class=None, no_stop=None, tag=None, deferred=None):
        sms_class = sms_class or self.sms_class
        no_stop = no_stop if no_stop is not None else self.no_stop
        tag = tag or self.tag
        deferred = deferred if deferred is not None else self.deferred
        message = unicode(message).encode('utf-8')
        to = list(to)
        if not all(map(utils.is_int_phone_number, to)):
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
        if no_stop:
            params['noStop'] = 1
        if tag:
            params['tag'] = tag[:20]
        if deferred is not None:
            params['deferred'] = deferred.strftime('%H%M%d%m%Y')
        try:
            response = requests.get(self.url, params=params)
        except Exception, e:
            raise utils.SMSError('unable to request %r' % self.url, e)
        try:
            result = response.json()
        except Exception, e:
            raise utils.SMSError('response is not JSON', e)
        status = result['status']
        if status >= 200:
            if status == 201:
                raise utils.SMSError('missing parameter', result)
            if status == 202:
                raise utils.SMSError('invalid parameter', result)
            if status == 401:
                raise utils.SMSError('ip not authorized', result)
            raise utils.SMSError('unqualified error', result)
        return result
