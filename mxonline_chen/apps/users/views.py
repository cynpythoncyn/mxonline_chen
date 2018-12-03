from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import JsonResponse

from utils.email_send import send_register_email
from .models import Userprofile, EmailVerifyRecord
from .forms import Login_form, RegisterForm, ForgetForm, ModifyForm, UploadImageForm
from utils.mixin_login import LoginRequiredMixin


# Create your views here.


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    获取邮箱验证码
    """

    def get(self, request):
        email = request.GET.get('email', '')
        if Userprofile.objects.filter(email=email):
            return JsonResponse({'email': '邮箱已存在！'})

        send_register_email(email=email, send_type='update_email')
        return JsonResponse({'status': 'success'})


class UpdateEmailView(LoginRequiredMixin, View):
    """
    个人中心，用户修改邮箱
    """

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'email': '验证码错误！', })


class UpdatePwdView(View):
    """
    个人中心用户修改密码
    """

    def post(self, request):
        modifyform = ModifyForm(request.POST)
        if modifyform.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 == pwd2:
                user = request.user
                user.password = make_password(pwd2)
                user.save()
                return JsonResponse({'status': 'success'})

            else:
                return JsonResponse({'status': 'fail', 'msg': '密码不一致'})
        else:
            return JsonResponse(modifyform.errors)


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """

    def post(self, request):
        uploadimage = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if uploadimage.is_valid():
            # 如果不传入instance，
            # userimage = uploadimage.cleaned_data['image']
            # request.user.image = userimage
            # request.user.save()
            uploadimage.save()
            return JsonResponse({
                "status": "success"
            })
        return JsonResponse({"status": "fail"})


class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人中心
    """

    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })



class ModifyPwdView(View):
    """
    修改密码接口
    """

    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '密码不一致！'})

            user = Userprofile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'modify_form': modify_form, 'email': email})


class ResetPwdView(View):
    """
    重置密码接口
    """

    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
            else:
                return render(request, 'active_fail.html')
        else:
            return render(request, 'login.html')


class ForgetPwdView(View):
    """
    忘记密码接口
    """

    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {"forget_form": forget_form, })

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")

            send_register_email(email, send_type='forget')
            return render(request, 'success_send.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


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
                return render(request, 'register.html', {'msg': '用户已存在！', "register_form": register_form})
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
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {"msg": "用户未激活！"})
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
