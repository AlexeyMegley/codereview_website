from django.urls import path, include, re_path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('sign_up', views.sign_up, name='sign_up'),
]