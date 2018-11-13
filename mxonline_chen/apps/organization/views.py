from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import CourseOrg,CityDict


class OrglistView(View):
    """
    课程机构列表接口
    """
    def get(self,request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 城市
        all_citys = CityDict.objects.all()
        # 机构数量
        org_nums = CourseOrg.objects.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs,1,request=request)

        orgs_c = p.page(page)


        return render(request,'org-list.html',{
            "all_orgs":orgs_c,
            "all_citys":all_citys,
            "org_nums":org_nums,
        })