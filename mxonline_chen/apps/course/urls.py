from django.conf.urls import url


from .views import CourselistView,CoursedetailView

urlpatterns = [
    # 课程列表页url
    url(r'^list/$', CourselistView.as_view(), name='list'),
    url(r'^detail/(?P<course_id>\d+)/$', CoursedetailView.as_view(), name='detail'),
]
