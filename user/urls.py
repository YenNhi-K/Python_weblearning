# from django.contrib import admin
from django.urls import path
from . import views

# app_name = "english_test"

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('test/', views.test, name='test'),
    path('file/', views.file, name='file'),
    path('list/', views.list_test, name='list'),
    path('history/<int:test_id>/', views.history, name='history'),
    path('list/<int:test_id>/', views.voca_list, name='voca-list'),
    path('delete/', views.delete_test, name='delete'),
    path('change-password/', views.change_password, name='change_password'),
]
