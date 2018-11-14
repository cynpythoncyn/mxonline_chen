
from django.conf.urls import url

from .views import OrglistView,UseraskView

urlpatterns = [
    # 课程机构列表页url
    url(r'^list/$', OrglistView.as_view(), name='list'),
    url(r'^addask/$', UseraskView.as_view(), name='add_ask'),

]