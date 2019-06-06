# import logging
from django.shortcuts import render
from django.http import HttpResponse
from torch.permission import check_permission
# from django.http import Http404
from lib.server import Server

# logger = logging.getLogger(__name__)
# 生成一个名为collect的logger实例
# collect_logger = logging.getLogger("collect")

@check_permission
def index(request):
    return render(request, 'torch/index.html')


@check_permission
def test(request):
    return render(request, 'html/404.html')

@check_permission
def plant_status(request):
    context = {'plants_status': Server().get_plants_status()}
    return render(request, 'torch/plant_status.html', context)