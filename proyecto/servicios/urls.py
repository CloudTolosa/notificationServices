from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_list, name='home_list'),
    path('sent_message', views.sent_message, name='sent_message'),
]