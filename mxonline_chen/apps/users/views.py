from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import JsonResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse

from pure_pagination import PageNotAnInteger,Paginator

from utils.email_send import send_register_email
from .models import Userprofile, EmailVerifyRecord, Banner
from .forms import Login_form, RegisterForm, ForgetForm, ModifyForm, UploadImageForm, UpdateInfoForm
from utils.mixin_login import LoginRequiredMixin
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from course.models import Course


# Create your views here.

class MymessageView(LoginRequiredMixin,View):
    """
    个人中心，我的消息
    """
    def get(self,request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空未读消息的记录
        all_unread_msgs = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_msg in all_unread_msgs:
            unread_msg.has_read = True
            unread_msg.save()

        # 个人消息分页的功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages,3,request=request)
        all_messages = p.page((page))

        return render(request,'usercenter-message.html',{
            "all_messages":all_messages,

        })


class MyfavCourseView(LoginRequiredMixin,View):
    """
    个人中心，我的收藏课程
    """
    def get(self,request):
        courses_list = []
        fav_cousers = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_couser in fav_cousers:
            course_id = fav_couser.fav_id
            course = Course.objects.get(id=course_id)
            courses_list.append(course)
        return render(request,'usercenter-fav-course.html',{
            "courses_list":courses_list,
        })


class MyfavTeacherView(LoginRequiredMixin,View):
    """
    用户中心，我的收藏讲师
    """
    def get(self,request):
        teachers_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id

            teacher = Teacher.objects.get(id=teacher_id)
            teachers_list.append(teacher)

        return render(request,'usercenter-fav-teacher.html',{
            "teachers_list":teachers_list

        })


class MyfavOrgView(LoginRequiredMixin,View):
    """
    用户中心，我的收藏机构
    """
    def get(self, request):
        orgs_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            orgs_list.append(org)

        return render(request, 'usercenter-fav-org.html', {
            "orgs_list":orgs_list
        })


class MycourseView(LoginRequiredMixin,View):
    """
    用户中心，我的课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses
        })


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

    def post(self, request):
        update_info = UpdateInfoForm(request.POST, instance=request.user)
        if update_info.is_valid():
            update_info.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse(update_info.errors)


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

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = userporfile.id
            user_message.message = "欢迎注册本网站"
            user_message.save()

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
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, 'login.html', {"msg": "用户未激活！"})
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误！"})

        else:

            return render(request, 'login.html', {"loginform": loginform})


class LogoutView(View):
    """
    用户登出接口
    """
    def get(self,request):
        logout(request)

        return HttpResponseRedirect(reverse("index"))


class IndexView(View):
    # 慕学在线网 首页
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        couser_orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            "all_banners":all_banners,
            "courses":courses,
            "banner_courses":banner_courses,
            "couser_orgs":couser_orgs,

        })



def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response