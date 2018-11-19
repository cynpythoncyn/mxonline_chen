from django.conf.urls import url

from .views import OrglistView, UseraskView, Org_homeView, Org_courseView, Org_descView,Org_teacherView
from .views import AddfavView,TeacherlistView
urlpatterns = [
    # 课程机构列表页url
    url(r'^list/$', OrglistView.as_view(), name='list'),
    url(r'^addask/$', UseraskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', Org_homeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', Org_courseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', Org_descView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/$', Org_teacherView.as_view(), name='org_teacher'),

    # 用户收藏
    url(r'^add_fav',AddfavView.as_view(),name='add_fav'),

    # 授课讲师列表页url 配置
    url(r'^teacher/list/$',TeacherlistView.as_view(),name='teacher_list')
]
