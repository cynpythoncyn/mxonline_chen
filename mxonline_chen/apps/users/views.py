from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from utils.email_send import send_register_email
from .models import Userprofile, EmailVerifyRecord
from .forms import Login_form, RegisterForm


# Create your views here.
class AciveUserView(View):
    """
    用户激活邮箱接口
    """
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = Userprofile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")

class RegisterView(View):
    """
    注册逻辑接口
    """

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("email", "")
            if Userprofile.objects.filter(email=username):
                return render(request, 'register.html', {'msg': '用户已存在！'})
            password = request.POST.get('password', '')

            userporfile = Userprofile()
            userporfile.username = username
            userporfile.email = username
            userporfile.is_active = False
            userporfile.password = make_password(password)
            userporfile.save()

            send_register_email(username, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {"register_form": register_form})


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

        loginform = Login_form(request.POST)
        if loginform.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误！"})

        else:
            return render(request, 'login.html', {"loginform": loginform})


class IndexView(View):
    # 慕学在线网 首页
    def get(self, request):
        # 取出轮播图

        return render(request, 'index.html', {

        })
