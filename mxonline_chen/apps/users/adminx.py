import xadmin
from users.models import EmailVerifyRecord,Banner
from xadmin import views


class BaseSetting(object):
    """
    增加后台主题功能
    """
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    """
    后台全局配置
    """
    site_title = "慕学cyn后台管理系统"
    site_footer = "慕学cyn在线网"
    menu_style = "accordion"


class EmailVerifyRecordadmin(object):

    list_display = ['code','email','send_type','send_time',]
    search_fields = ['code','email','send_type',]
    list_filter = ['code','email','send_type','send_time',]
    model_icon = 'fa fa-address-book-o'


class Banneradmin(object):

    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordadmin)
xadmin.site.register(Banner,Banneradmin)


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

