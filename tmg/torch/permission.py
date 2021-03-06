import logging
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from torch import models
from django.db.models import Q
from django.urls import resolve  # 此方法可以将url地址转换成url的name

logger = logging.getLogger(__name__)

def perm_check(request, *args, **kwargs):
    url_obj = resolve(request.path_info)
    url_name = url_obj.url_name
    # 权限必须和urlname配合使得
    if url_name and request.user:
        if not request.user.is_authenticated:
            return False
        # 获取请求方法，和请求参数
        # url_method, url_args = request.method, request.GET

        get_perm = [item.permission.url for item in models.UserPermission.objects.filter(Q(user=request.user))]

        if get_perm and url_name in get_perm:
            return True
        else:
            logger.error('用户：%s 无访问%s的权限' % (request.user, request.get_full_path()))
            return False
    else:
        logger.error('无访问权限')
        return False  # 没有权限设置，默认不放过


def check_permission(fun):  # 定义一个装饰器，在views中应用
    def wapper(request, *args, **kwargs):
        logger.info('用户:%s 访问 url: %s' % (request.user, request.get_full_path()))
        if perm_check(request, *args, **kwargs):  # 调用上面的权限验证方法
            return fun(request, *args, **kwargs)
        return HttpResponse('无访问权限！', status=403)
    return wapper
