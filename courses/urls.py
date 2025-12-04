from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
]