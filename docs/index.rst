.. django_wechat documentation master file, created by
   sphinx-quickstart on Sat Apr  9 15:12:39 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django_wechat
=============

django_wechat 是一个基于django的微信基础模块,提供了微信的最基础接口功能.

功能
-----

- 关注回复(关键字为"关注")
- 默认回复(关键字为"默认")
- 文本回复
- 单图文回复
- 自定义菜单

使用方法
---------

安装依赖模块::

    pip install xmltodict

安装wechat::

    pip install git+https://github.com/ChanMo/django_wechat.git

把wechat模块添加到你的settings.py里面::

    INSTALLED_APPS = (
        ...
        'wechat',
        ...
   ) 


在settings.py里面添加微信设置信息::

    # wechat config
    WECHAT_APPID = 'test'
    WECHAT_APPSECRET = 'test'
    WECHAT_TOKEN = 'yourtoken'
    WECHAT_MCH_ID = 'test'
    WECHAT_KEY = 'test'
    WECHAT_JS_DEBUG = 'test'
    WECHAT_JS_APILIST = ['test']
    
在urls.py里面添加微信接口::

    url(r'^wx/', include('wechat.urls')),

添加数据表::

   python manage.py migrate

使用微信开发者模块::

   接口地址为：http://yourdomain/wx/
   token为: yourtoken


api模块
--------

- Base
- Menu 
- Push
- Reponse 
- Member 
- Pay
- Js 
- Qrcode


开发者
-------

- chanmo: http://www.findchen.com/

版本更改
---------
- v0.3 使js配置信息可编辑，添加Qrcode类
- v0.2 添加WxMemberView
- v0.1 第一版
