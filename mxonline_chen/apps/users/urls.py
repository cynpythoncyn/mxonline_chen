
from django.conf.urls import url,include

from .views import UserinfoView

urlpatterns = [
    url(r'^info/$',UserinfoView.as_view(),name='userinfo'),

]

