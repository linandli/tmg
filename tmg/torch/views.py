from django.shortcuts import render
from django.http import HttpResponse
from torch.permission import check_permission
# from django.http import Http404


@check_permission
def index(request):
    return render(request, 'torch/index.html')
    # return HttpResponse('你好')


@check_permission
def test(request):
    return render(request, 'html/404.html')
    # return HttpResponse('Test')

