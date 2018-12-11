import xadmin

from .models import CourseOrg,CityDict,Teacher


class CourseOrgadmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']

    # xadmin的进阶开发
    relfield_style = 'fk-ajax' # 动态加载的方式



class CityDictadmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']

class Teacheradmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']


xadmin.site.register(CourseOrg,CourseOrgadmin)
xadmin.site.register(CityDict,CityDictadmin)
xadmin.site.register(Teacher,Teacheradmin)