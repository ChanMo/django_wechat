#!/usr/bin/python
# vim: set fileencoding=utf-8 :
import json
from django.db import models

class Menu(models.Model):
    TYPE_CHOICES = (
        ('null', '根目录'),
        ('view', '跳转URL'),
        ('click', '点击推事件'),
    )
    top = models.ForeignKey('self', related_name='Top', verbose_name='主菜单', blank=True, null=True, default=None)
    name = models.CharField(max_length=100, verbose_name='名称')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='view', verbose_name='类型')
    value = models.CharField(max_length=200, verbose_name='值', blank=True, null=True, default='')
    sort = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='排序')

    def __unicode__(self):
        return self.name

    class Meta(object):
        verbose_name = '自定义菜单'
        verbose_name_plural = '自定义菜单'
        ordering = ['sort']


class Text(models.Model):
    keyword = models.CharField(max_length=20, verbose_name='关键字')
    content = models.TextField(verbose_name='内容')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __unicode__(self):
        return self.keyword

    class Meta(object):
        verbose_name = '文本回复'
        verbose_name_plural = '文本回复'
        ordering = ['-updated']


class News(models.Model):
    keyword = models.CharField(max_length=20, verbose_name='关键字')
    title = models.CharField(max_length=200, verbose_name='标题')
    description = models.TextField(verbose_name='描述')
    pic = models.ImageField(upload_to='wechat/', verbose_name='图片')
    url = models.URLField(max_length=200, verbose_name='链接')
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __unicode__(self):
        return self.keyword

    class Meta(object):
        verbose_name = '图文回复'
        verbose_name_plural = '图文回复'
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
