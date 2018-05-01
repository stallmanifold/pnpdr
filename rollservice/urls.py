from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rollservice import views


urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^dice_seq/', 
        views.DiceSequenceList.as_view(),
        name='dice-seq'
    ),
    url(r'^rolls/', 
        views.RollSequenceList.as_view(),
        name='roll-seq'
    ),
    url(r'^users/$', 
        views.UserList.as_view(), 
        name='user-list'
    ),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(), 
        name='user-detail'
    ),
])

