from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages


def home(request):
    """Homepage showing all courses"""
    courses = Course.objects.all()
    return render(request, 'courses/home.html', {'courses': courses})


def course_detail(request, slug):
    """Individual course page with lesson list"""
    course = get_object_or_404(Course, slug=slug)
    lessons = course.lessons.filter(is_published=True)
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons
    })


def lesson_detail(request, course_slug, lesson_slug):
    """Individual lesson page"""
    lesson = get_object_or_404(
        Lesson, 
        course__slug=course_slug, 
        slug=lesson_slug,
        is_published=True
    )
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})

def register(request):
    """Simple user registration view using Django's UserCreationForm."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Account created and logged in as {user.username}.")
            return redirect(settings.LOGIN_REDIRECT_URL or 'courses:home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

# Optional: Login-required view example
@login_required
def my_courses(request):
    """Show courses for logged-in users"""
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'courses/my_courses.html', {'courses': courses})

