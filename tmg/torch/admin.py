from django.contrib import admin
from torch import models

# Register your models here.

class PermissionAdmin(admin.ModelAdmin):
    # 需要显示的字段信息
    list_display = ('id', 'name', 'url', 'per_method', 'describe')
    # 设置哪些字段可以点击进入编辑界面，默认是第一个字段
    list_display_links = ('id', 'name', 'url')

class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'permission_id')
    list_display_links = ('user_id',)

admin.site.register(models.Permission, PermissionAdmin)
admin.site.register(models.UserPermission, UserPermissionAdmin)
