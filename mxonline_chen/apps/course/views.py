from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from .models import Course,CourseResource
from operation.models import UserFavorite


class CourselessonView(View):
    """
    章节详情页
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # course_resc = course.courseresource_set.all()
        # 这两种查询方式得到的结果一样
        course_resc = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resc': course_resc,
        })


class CoursedetailView(View):
    """
    课程详情页
    """

    def get(self, request, course_id):

        all_course = Course.objects.get(id=int(course_id))

        # 增加课程点击数
        all_course.click_nums += 1
        all_course.save()

        # 是否收藏课程
        has_fav_course = False
        # 是否收藏机构
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=all_course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=all_course.course_org.id):
                has_fav_org = True

        # 相关课程推荐
        tag = all_course.tag
        if tag:

            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request, 'course-detail.html', {
            'course': all_course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
        })


class CourselistView(View):
    """
    课程列表页
    """

    def get(self, request):
        # 取出所有课程
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        sort = request.GET.get('sort', '')
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

        course_p = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': course_p,
            'sort': sort,
            'hot_courses': hot_courses,

        })
