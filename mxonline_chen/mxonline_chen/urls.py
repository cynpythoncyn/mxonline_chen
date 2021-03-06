"""mxonline_chen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from users.views import IndexView, LoginView, RegisterView, AciveUserView, ForgetPwdView, ResetPwdView, ModifyPwdView,LogoutView
from organization.views import OrglistView
from mxonline_chen.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    # url(r'^login/$',login_chen,name='login'),
    # url(r'^login/$',TemplateView.as_view(template_name='login.html'),name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', AciveUserView.as_view(), name='user_active'),
    url(r'^forget_pwd/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetPwdView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构url相关配置
    url(r'^org/',include('organization.urls',namespace='org')),

    # 课程相关url配置
    url(r'^course/',include('course.urls',namespace='course')),

    # 配置上传图片的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 自定义静态文件路径
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # 配置用户个人中心
    url(r'^users/',include('users.urls',namespace='users')),

    # ueditor 富文本编辑器相关url
    url(r'^ueditor/',include('DjangoUeditor.urls' )),

]
#全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'