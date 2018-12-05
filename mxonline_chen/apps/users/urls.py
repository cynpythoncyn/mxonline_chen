
from django.conf.urls import url,include

from .views import UserinfoView,UploadImageView,UpdatePwdView,UpdateEmailView,SendEmailCodeView,MycourseView
from .views import MyfavOrgView,MyfavTeacherView,MyfavCourseView



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

    # 用户中心我的课程
    url(r'^mycourse/$',MycourseView.as_view(),name='mycourse'),

    # 用户中心我的收藏课程机构
    url(r'^myfav/org/$', MyfavOrgView.as_view(), name='myfav_org'),

    # 用户中心我的收藏授课讲师
    url(r'^myfav/teacher/$', MyfavTeacherView.as_view(), name='myfav_teacher'),

    # 用户中心我的收藏公开课程
    url(r'^myfav/couser/$', MyfavCourseView.as_view(), name='myfav_course'),


]

