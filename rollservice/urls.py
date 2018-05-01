from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from rollservice import views

schema_view = get_schema_view(title='PNP Die Roller API')

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
    url(r'^schema/$', schema_view),
])

