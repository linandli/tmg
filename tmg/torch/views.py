# from django.shortcuts import render
from django.http import HttpResponse

from rest_framework_jwt.compat import get_user_model


# Create your views here.
def index(request):
    return HttpResponse('This is index.')

#views中重写authenticate认证

# from django.contrib.auth.backends import ModelBackend
# User=get_user_model()
#
# # Create your views here.
# class CustomBackend(ModelBackend):
#    '''
#    自定义用户验证(setting.py)
#    '''
#    def authenticate(self, username=None, password=None, **kwargs):
#        try:
#            user=UserProfile.objects.get(Q(username=username)|Q(mobile=username))
#            if user.check_password(password):
#            　　return user
#        except Exception as e:
#            return None