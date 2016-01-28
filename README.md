# Wechat

Wechat is a module based django and wechat api.

Detailed documentation is in the "docs" directory

## Quick start

1. Add "wechat" to your INSTALLED_APPS setting like this:
    ```
    INSTALLED_APPS = (
        ...
        'wechat',
    )
   ```

2. Add wechat config to your settings.py file:
    ```
    # wechat config
    WECHAT_APPID = ''
    WECHAT_APPSECRET = ''
    WECHAT_TOKEN = ''
    WECHAT_MCH_ID = ''
    WECHAT_KEY = ''
    WECHAT_JS_DEBUG = ''
    WECHAT_JS_APILIST = []
    ```

2. Include the wechat URLconf in your project urls.py like this:
   `url(r'^wechat/', include('wechat.urls')),`

3. Run `python manage.py migrate` to create the wechat models.

4. Add url `http://yourdomain/wechat/` and `yourtoken` to your wechat dashboard.


## Changelog

> v0.3 -make jsapi editable, fixed get_code_url()
> v0.2 -create base view
> v0.1 -initial release
