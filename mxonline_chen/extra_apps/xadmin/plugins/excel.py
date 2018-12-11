# coding:utf-8
from django.urls import reverse

import xadmin
from xadmin.plugins.utils import get_context_dict
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader



#
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        context = get_context_dict(context or {})  # no error!
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context=context))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)