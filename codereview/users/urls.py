from django.urls import path, include, re_path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('log_in', views.log_in, name='login'),
    path('log_out', views.log_out, name='logout'),
    path('sign_up', views.sign_up, name='sign_up'),
]