from django.urls import path
from . import views

# app_name = 'user'

urlpatterns = [
    path('', views.import_file, name='import_file'),
    path('test/', views.test, name='test'),
    path('check/', views.check, name='check'),
    path('home/', views.test_home, name='home'),
    path('test_check/<int:no_question>/<int:no_correct>/', views.test_check, name='test_check'),
    path('quiz_check/<int:no_question>/<int:no_correct>/', views.quiz_check, name='quiz_check'),
]
