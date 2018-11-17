from django.conf.urls import url


from .views import CourselistView,CoursedetailView,CourselessonView

urlpatterns = [
    # 课程列表页url
    url(r'^list/$', CourselistView.as_view(), name='list'),

    url(r'^detail/(?P<course_id>\d+)/$', CoursedetailView.as_view(), name='detail'),

    url(r'^lesson/(?P<course_id>\d+)/$', CourselessonView.as_view(), name='lesson'),
]
