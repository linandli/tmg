from django.shortcuts import render
from django.http import HttpResponse
from torch.permission import check_permission

@check_permission
def index(request):
    return HttpResponse('你好')