基于django的微信基础模块
========================

此版本已停止更新，把功能进行拆分，分为 `django-wechat-base <http://github.com/ChanMo/django-wechat-base.git>`_，`django-wechat-message <http://github.com/ChanMo/django-wechat-message.git>`_，`django-wechat-menu <http://github.com/ChanMo/django-wechat-menu.git>`_，同时 `django-wechat-member <http://github.com/ChanMo/django-wechat-member.git>`_， `django-wechat-pay <http://github.com/ChanMo/django-wechat-pay.git>`_， `django-wechat-qrcode <http://github.com/ChanMo/django-wechat-qrcode.git>`_ 等模块也进行相应更新。

.. image:: https://readthedocs.org/projects/django-wechat/badge/?version=latest
    :target: http://django-wechat.readthedocs.org/zh_CN/latest/?badge=latest
    :alt: Documentation Status

一个基于django的微信基础功能模块

快速开始:
---------

安装wechat:

.. code-block::

    pip install django-wechat-base

把wechat模块添加到你的settings.py里面:

.. code-block::

    INSTALLED_APPS = (
        ...
        'wechat',
        ...
    )

在settings.py里面添加微信设置信息:

.. code-block::

    # wechat config
    WECHAT_APPID = 'test'
    WECHAT_APPSECRET = 'test'
    WECHAT_TOKEN = 'yourtoken'
    WECHAT_MCH_ID = 'test'
    WECHAT_KEY = 'test'
    WECHAT_JS_DEBUG = 'test'
    WECHAT_JS_APILIST = ['test']
    
在urls.py里面添加微信接口:

.. code-block::

    url(r'^wx/', include('wechat.urls')),

添加数据表:

.. code-block::

   python manage.py migrate

使用微信开发者模块:

   接口地址为：http://yourdomain/wx/
   token为: yourtoken



版本更改:
---------
- v0.4 添加多语言支持
- v0.3 使js配置信息可编辑，添加Qrcode类
- v0.2 添加WxMemberView
- v0.1 第一版
