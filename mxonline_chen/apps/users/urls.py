
from django.conf.urls import url,include

from .views import UserinfoView,UploadImageView,UpdatePwdView

urlpatterns = [
    # 用户个人中心首页
    url(r'^info/$',UserinfoView.as_view(),name='userinfo'),

    # 用户修改头像
    url(r'^image/upload$',UploadImageView.as_view(), name='image_upload'),

    # 用户修改密码
    url(r'^update/pwd/$',UpdatePwdView.as_view(), name='update_pwd')

]

