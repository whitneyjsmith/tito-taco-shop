from django.urls import path, include
from . import views

urlpatterns = [
    #path('slack', views.oauth, name='slack-oauth'),
    path('', views.index),
    path('slack/oauth/', views.slack_oauth)
]