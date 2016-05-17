import json

from django.contrib import admin
from . import models
from .models import Menu, Text, News
from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from . import api


class MenuAdmin(admin.ModelAdmin):
    list_display = ('top', 'name', 'type', 'value')

    def get_urls(self):
        urls = super(MenuAdmin, self).get_urls()
        my_urls = [
            url(r"^sync/$", self.sync_menu),
        ]
        return my_urls + urls

    def sync_menu(self, request):
        menu_list = models.menu_list()
        wx = api.Menu()
        content = wx.sync_menu(menu_list)
        return HttpResponse(json.dumps(content))

    def get_form(self, request, obj=None, **kwargs):
        form = super(MenuAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['top'].queryset = Menu.objects.filter(top=None)
        return form


class TextAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'content', 'updated')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'title', 'description', 'updated')


admin.site.register(Menu, MenuAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(News, NewsAdmin)
