from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator,PageNotAnInteger

from .models import Course
class CourselistView(View):
    """
    课程列表页
    """
    def get(self,request):
        # 取出所有课程
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        sort = request.GET.get('sort','')
        if sort == 'student':
            all_courses = all_courses.order_by('-students')
        elif sort == 'hot':
            all_courses = all_courses.order_by(('-click_nums'))

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        course_p= p.page(page)

        return render(request,'course-list.html',{
            'all_courses':course_p,
            'sort':sort,
            'hot_courses':hot_courses,


        })