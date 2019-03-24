# from django.contrib import admin
import xadmin

# Register your models here.
from xadmin import views


class GlobalSetting(object):
    site_title = '后台管理'
    site_footer = '西安图迹信息科技有限公司'
    menu_style = "accordion"


xadmin.site.register(views.CommAdminView, GlobalSetting)
