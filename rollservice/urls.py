from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rollservice import views


urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^dice_seq/', views.DiceSequenceList.as_view()),
    url(r'^rolls/', views.RollSequenceList.as_view()),
])

