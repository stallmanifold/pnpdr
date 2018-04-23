from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rollservice import views


urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^dice_seq/', views.DiceSequenceList.as_view()),
    url(r'^die_seq/', views.DiceSequenceList.as_view()),
    url(r'^rolls/', views.RollSequenceList.as_view()),
    url(r'^users/$', 
        views.UserList.as_view(), 
        name='user-list'
    ),
    url(r'^users/(?P<pk>[0-9]+)/$', 
        views.UserDetail.as_view(), 
        name='user-detail'
    ),
])

