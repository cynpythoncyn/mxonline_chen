
from django.conf.urls import url

from .views import OrglistView,UseraskView,Org_homeView,Org_courseView

urlpatterns = [
    # 课程机构列表页url
    url(r'^list/$', OrglistView.as_view(), name='list'),
    url(r'^addask/$', UseraskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', Org_homeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', Org_courseView.as_view(), name='org_course'),

]