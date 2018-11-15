from django.conf.urls import url


from .views import CourselistView

urlpatterns = [
    # 课程列表页url
    url(r'^list/$', CourselistView.as_view(), name='list'),
]
