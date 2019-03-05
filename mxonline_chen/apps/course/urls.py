from django.conf.urls import url


from .views import CourselistView,CoursedetailView,CourselessonView,CommentView,Add_commentView,Video_playView

urlpatterns = [
    # 课程列表页url
    url(r'^list/$', CourselistView.as_view(), name='list'),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CoursedetailView.as_view(), name='detail'),
    # 课程章节页
    url(r'^lesson/(?P<course_id>\d+)/$', CourselessonView.as_view(), name='lesson'),

    # 课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name='comment'),
    # 添加课程评论
    url(r'^add_comment/$', Add_commentView.as_view(), name='add_comment'),

    # 视频播放url
    url(r'^video/(?P<video_id>\d+)/$', Video_playView.as_view(), name='video_play'),

]
# 这是test