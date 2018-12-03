
from django.conf.urls import url,include

from .views import UserinfoView,UploadImageView,UpdatePwdView,UpdateEmailView,SendEmailCodeView
urlpatterns = [
    # 用户个人中心首页
    url(r'^info/$',UserinfoView.as_view(),name='userinfo'),

    # 用户修改头像
    url(r'^image/upload$',UploadImageView.as_view(), name='image_upload'),

    # 用户修改密码
    url(r'^update/pwd/$',UpdatePwdView.as_view(), name='update_pwd'),

    # 发送邮箱验证码
    url(r'^send_email_code_change/$',SendEmailCodeView.as_view(), name='send_email_code_change'),

    # 用户修改邮箱
    url(r'^update_email/$',UpdateEmailView.as_view(), name='update_email'),


]

