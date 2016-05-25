import json
from django.utils.translation import ugettext_lazy as _
from django.db import models

class Menu(models.Model):
    TYPE_CHOICES = (
        ('null', _('root menu')),
        ('view', _('view menu')),
        ('click', _('click menu')),
    )
    top = models.ForeignKey('self', related_name='children', blank=True,\
            null=True, default=None, verbose_name=_('root menu'))
    name = models.CharField(_('name'), max_length=100)
    type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES,\
            default='view')
    value = models.CharField(_('value'), max_length=200, blank=True,\
            null=True, default='')
    sort = models.PositiveIntegerField(_('sort'), blank=True, null=True,\
            default=0)

    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = _('menu')
        verbose_name_plural = _('menus')
        ordering = ['sort']


class Text(models.Model):
    keyword = models.CharField(_('keyword'), max_length=20)
    content = models.TextField(_('content'))
    created = models.DateTimeField(_('created time'), auto_now_add=True)
    updated = models.DateTimeField(_('updated time'), auto_now=True)

    def __unicode__(self):
        return self.keyword

    class Meta(object):
        verbose_name = _('text response')
        verbose_name_plural = _('text response')
        ordering = ['-updated']


class News(models.Model):
    keyword = models.CharField(_('keyword'), max_length=20)
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'))
    pic = models.ImageField(_('image'), upload_to='upload/wechat/%Y/%m/%d')
    url = models.URLField(_('link'), max_length=200)
    created = models.DateTimeField(_('created time'), auto_now_add=True)
    updated = models.DateTimeField(_('updated time'), auto_now=True)

    def __unicode__(self):
        return self.keyword

    class Meta(object):
        verbose_name = _('news response')
        verbose_name_plural = _('news response')
        ordering = ['-updated']


def menu_list():
    top = Menu.objects.order_by('sort').filter(top=None)
    button = {'button':[]}
    for i, item in enumerate(top):
        children = Menu.objects.order_by('sort').filter(top=item)
        if children:
            sub_button = []
            for j, chil_item in enumerate(children):
                sub_button.append(item_menu(chil_item))
            button['button'].append({
                'name': item.name,
                'sub_button': sub_button,
            })
        else:
            button['button'].append(item_menu(item))
    button = json.dumps(button, ensure_ascii=False)
    button = button.encode('utf8')
    return button

def item_menu(menu):
    if menu.type == 'view':
        button = {
            'name': menu.name,
            'type': menu.type,
            'url': menu.value,
        }
    elif menu.type == 'click':
        button = {
            'name': menu.name,
            'type': menu.type,
            'key': menu.value,
        }
    elif menu.type == 'null':
        button = {
            'name': menu.name,
        }
    return button
