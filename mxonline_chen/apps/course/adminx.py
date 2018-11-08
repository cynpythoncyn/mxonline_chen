import xadmin

from .models import Course, Lesson, Video, CourseResource


class Courseadmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', ]
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']


class Lessonadmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class Videoadmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceadmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, Courseadmin)
xadmin.site.register(Lesson, Lessonadmin)
xadmin.site.register(Video, Videoadmin)
xadmin.site.register(CourseResource, CourseResourceadmin)
