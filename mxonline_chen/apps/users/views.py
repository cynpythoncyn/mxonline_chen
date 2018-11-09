from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import Userprofile


# Create your views here.

class CustomBackend(ModelBackend):
    """
    重写authenticate方法
    """

    def authenticate(self, username=None, password=None, **kwargs):

        try:
            user = Userprofile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    """
    慕学网登陆页面接口
    """
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {})


def login_chen(request):
    # 这是函数形式的登陆接口
    if request.method == "POST":
        pass
    elif request.method == 'GET':
        return render(request, "login.html", {})


class IndexView(View):
    # 慕学在线网 首页
    def get(self, request):
        # 取出轮播图

        return render(request, 'index.html', {

        })
