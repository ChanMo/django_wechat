import os
import hashlib
import urllib
import urllib2
import json
import time
import datetime
import random
import string
import collections

from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import localtime
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.conf import settings

import xmltodict #pip install xmltodict

from .models import Menu, Text, News


class Base(object):
    'base class'
    base_url = 'https://api.weixin.qq.com/cgi-bin/'
    appid = ''
    appsecret = ''
    token = ''

    def __init__(self):
        self.appid = settings.WECHAT_APPID
        self.appsecret = settings.WECHAT_APPSECRET
        self.token = settings.WECHAT_TOKEN

    def get_token(self):
        access_token = cache.get('wx_access_token')
        if access_token:
            return access_token
        else:
            param = {
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.appsecret,
            }
            url = self.get_url('token', param)
            data = self.get_data(url)
            cache.set('wx_access_token', data['access_token'], int(data['expires_in']))
            return data['access_token']


    # get data
    def get_data(self, url, data='', return_json=True):
        result = urllib2.urlopen(url, data)
        string = result.read()
        result.close()
        if return_json:
            json_data = json.loads(string)
            return json_data
        else:
            return string


    # get random string
    def get_random(self, length=32):
        result = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        return result

    # get sign
    def get_sign(self, data):
        data = collections.OrderedDict(sorted(data.items()))
        s = ''
        for item in data:
            s = s + item + '=' + data[item] + '&'
        s = s[0:-1]
        s +=  '&key=%s' % self.key
        s = hashlib.md5(s).hexdigest()
        ss = s.upper()
        return ss

    # check sign
    def check_sign(self, data):
        s = [self.token, data['timestamp'], data['nonce']]
        s.sort()
        ss = ''.join(s)
        new_sign = hashlib.sha1(ss.encode('utf-8')).hexdigest()
        if data['signature'] == new_sign:
            return data['echostr']
        else:
            return False

    # get api url
    def get_url(self, api, param, other=''):
        url_string = urllib.urlencode(param)
        if 'http' in api:
            url = api + '?' + url_string + other
        else:
            url = self.base_url + api + '?' + url_string + other
        return url


    def dict_to_xml(self, data, s=''):
        for key, value in data.iteritems():
            if type(value).__name__ == 'dict':
                s = s + '<' + key + '>' + self.dict_to_xml(value, s) + '</' + key + '>'
            elif type(value).__name__ == 'int':
                s = s + '<' + key + '>' + unicode(value) + '</' + key + '>'
            else:
                s = s + '<' + key + '><![CDATA[' + value + ']]></' + key + '>'
        return s

class Menu(Base):
    'Menu'
    def sync_menu(self, menu):
        url = self.get_url('menu/create', {'access_token':self.get_token()})
        result = self.get_data(url, menu)
        return result



class Push(Base):
    'Template message'
    def push_message(self, data):
        url = self.get_url('message/template/send', {'access_token':self.get_token()})
        message = json.dumps(data)
        result = self.get_data(url, message)
        return result



class Response(Base):
    'response class'
    domain = ''
    receive_data = ''

    def __init__(self, request):
        self.domain = settings.WECHAT_DOMAIN
        data = request.body
        data = dict(xmltodict.parse(data)['xml'])
        self.receive_data = data

    def set_keyword(self):
        """
        set wechat message transfer to a keyword
        :param data: wechat data(dict)
        :return: keyword(str)
        """
        data = self.receive_data
        try:
            keyword = data['Content']
        except KeyError:
            try:
                if data['MsgType'] == 'event':
                    if data['Event'] == 'subscribe':
                        keyword = 'subscribe'
                    elif data['Event'] == 'CLICK':
                        keyword = data['EventKey']
                    else:
                        keyword = data['Event']
            except KeyError:
                keyword = 'default'

        self.keyword = keyword

    def get_response(self):
        self.set_keyword()
        try:
            news = News.objects.get(keyword=self.keyword)
            msg = self.response_news(news)
        except News.DoesNotExist:
            try:
                text = Text.objects.get(keyword=self.keyword)
                msg = self.response_text(text)
            except Text.DoesNotExist:
                text = Text.objects.get(keyword='default')
                msg = self.response_text(text)
        return msg

    def response_text(self, obj):
        data = self.receive_data
        message = {
            'xml': {
                'ToUserName': data['FromUserName'],
                'FromUserName': data['ToUserName'],
                'CreateTime': int(time.time()),
                'MsgType': 'text',
                'Content': obj.content,
            }
        }
        return self.dict_to_xml(message)

    def response_news(self, obj):
        data = self.receive_data
        message = {
            'xml': {
                'ToUserName': data['FromUserName'],
                'FromUserName': data['ToUserName'],
                'CreateTime': int(time.time()),
                'MsgType': 'news',
                'ArticleCount': 1,
                'Articles': {
                    'item': {
                        'Title': obj.title,
                        'Description': obj.description,
                        'PicUrl': 'http://' + self.domain + obj.pic.url,
                        'Url': obj.url,
                    }
                }
            }
        }
        return self.dict_to_xml(message)



class Member(Base):
    'member'
    def get_code_url(self, redirect_uri, state):
        redirect_uri = urllib.quote(redirect_uri, safe='')
        # url = 'https://open.weixin.qq.com/connect/oauth2/authorize'
        # param = {
        #     'appid': self.appid,
        #     'redirect_uri': redirect_uri,
        #     'response_type': 'code',
        #     'scope': 'snsapi_userinfo',
        #     'state': state,
        # }
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=%s#wechat_redirect' % (self.appid, redirect_uri, state)
        #return self.get_url(url)
        return url

    def get_access_token_url(self, code):
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        param = {
            'appid': self.appid,
            'secret': self.appsecret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        url = self.get_url(url, param)
        user = self.get_data(url)
        return user

    def get_user_info(self, code):
        user = self.get_access_token_url(code)
        url = 'https://api.weixin.qq.com/sns/userinfo'
        param = {
            'access_token': user['access_token'],
            'openid': user['openid'],
            'lang': 'zh_CN',
        }
        url = self.get_url(url, param)
        result = self.get_data(url)
        return result



class Pay(Base):
    'pay'
    mch_id = ''
    key = ''

    def __init__(self):
        super(Pay, self).__init__()
        self.mch_id = settings.WECHAT_MCH_ID
        self.key = settings.WECHAT_KEY


    def set_prepay_id(self, data):
        data['xml'].update({
            'trade_type': 'JSAPI',
            'appid': self.appid,
            'mch_id': self.mch_id,
            'nonce_str': unicode(self.get_random()),
        })
        data['xml']['sign'] = self.get_sign(data['xml'])
        #return json.dumps(data)
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        #message = xmltodict.unparse(new_data, pretty=True)
        message = self.dict_to_xml(data)
        result = self.get_data(url, message, False)
        data = dict(xmltodict.parse(result))
        self.prepay_id = data['xml']['prepay_id']


    def get_pay_data(self):
        data = {
            'appId': self.appid,
            'timeStamp': unicode(int(time.time())),
            'nonceStr': self.get_random(),
            'package': 'prepay_id=%s' % self.prepay_id,
            'signType': 'MD5',
        }
        sign = {'paySign': self.get_sign(data),}
        data.update(sign)
        data = json.dumps(data)
        return data


class Js(Base):
    'jssdk'

    def __init__(self):
        super(Js, self).__init__()
        self.jsapi = settings.WECHAT_JS_APILIST
        self.debug = settings.WECHAT_JS_DEBUG

    def get_ticket(self):
        jsapi_ticket = cache.get('wx_jsapi_ticket')
        if jsapi_ticket:
            return jsapi_ticket
        else:
            param = {
                'access_token': self.get_token(),
                'type': 'jsapi',
            }
            url = self.get_url('ticket/getticket', param)
            data = self.get_data(url)
            cache.set('wx_jsapi_ticket', data['ticket'], int(data['expires_in']))
            return data['ticket']

    def get_config(self, url):
        noncestr = self.get_random()
        timestamp = unicode(int(time.time()))
        sign = self.get_js_sign(url, noncestr, timestamp)
        wx_config = {
            'debug': self.debug,
            'appId': self.appid,
            'timestamp': timestamp,
            'nonceStr': noncestr,
            'signature': sign,
            #'jsApiList': ['onMenuShareTimeline','onMenuShareAppMessage'],
            'jsApiList': self.jsapi,
        }
        return json.dumps(wx_config)


    def get_js_sign(self, url, noncestr, timestamp):
        data = {
            'url': url,
            'noncestr': noncestr,
            'jsapi_ticket': self.get_ticket(),
            'timestamp': timestamp,
        }
        data = collections.OrderedDict(sorted(data.items()))
        s = ''
        for item in data:
            s = s + item + '=' + data[item] + '&'
        s = s[0:-1]
        s = hashlib.sha1(s).hexdigest()
        return s


class Qrcode(Base):
    'qrcode'
    def get_ticket(self, id):
        token = self.get_token()
        url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % token
        data = {
            'action_name': 'QR_LIMIT_SCENE',
            'action_info': {
                'scene': {
                    'scene_id': id,
                }
            }
        }
        data = json.dumps(data)
        result = self.get_data(url, data)
        return result['ticket']
