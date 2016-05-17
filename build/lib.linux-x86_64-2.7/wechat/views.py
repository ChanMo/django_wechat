#!/usr/bin/python
# vim: set fileencoding=utf-8 :
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import api


# Create your views here.
@csrf_exempt
def index(request):
    wx = api.Base()
    data = request.GET
    try:
        echostr = data['echostr']
        result = wx.check_sign(data)
        if result:
            return HttpResponse(echostr)
        else:
            return HttpResponse('error')
    except KeyError:
        wx_res = api.Response(request)
        result = wx_res.get_response()
        return HttpResponse(result)

