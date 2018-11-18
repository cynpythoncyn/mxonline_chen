from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComments,UserCourse
from utils.mixin_login import LoginRequiredMixin


class Add_commentView(View):
    """
    添加评论接口
    """

    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'fail', 'msg': '用户未登陆'})
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comment = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            return JsonResponse({'status': 'success', 'msg': '添加成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '添加失败'})


class CommentView(LoginRequiredMixin, View):
    """
    课程评论

    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        course_resc = course.courseresource_set.all()
        all_comments = CourseComments.objects.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_comments, 2, request=request)

        course_p = p.page(page)
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resc': course_resc,
            'all_comments': course_p,
        })


class CourselessonView(LoginRequiredMixin,View):
    """
    章节详情页
    """

    def get(self, request, course_id):
        # 根据前端传来的课程id，查找出课程
        course = Course.objects.get(id=int(course_id))

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        # 根据课程，查出所有学过这门课程的用户
        user_courses = UserCourse.objects.filter(course=course)

        # 使用python列表推导式查出所有用户的id
        user_ids = [user_course.user.id for user_course in user_courses]

        # 根据用户的id找出用户还学过的其它课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #然后查出相应课程的id
        course_ids = [us_course.course.id for us_course in all_user_courses]

        # 最后根据课程id，查询出学习该课程的用户还学过其它的课程
        relater_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        # course_resc = course.courseresource_set.all()
        # 这两种查询方式得到的结果一样
        course_resc = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resc': course_resc,
            'relater_courses': relater_courses,
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
