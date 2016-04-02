基于django的微信基础模块
========================

一个基于django的微信基础功能模块

快速开始:
---------

安装依赖模块:

.. code-block::

    pip install xmltodict

安装wechat:

.. code-block::

    pip install git+https://github.com/ChanMo/django_wechat.git

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
- v0.3 使js配置信息可编辑，添加Qrcode类
- v0.2 添加WxMemberView
- v0.1 第一版
