from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('<slug:slug>/subscribe/', views.toggle_subscription, name="toggle_subscription"),
    path('<slug:course_slug>/<slug:lesson_slug>/complete/', views.mark_read_and_next, name="mark_read_and_next"),
    path('<slug:course_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
]