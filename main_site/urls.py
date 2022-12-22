from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login/', views.login, name='login'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('post/', views.post, name='post'),
]
