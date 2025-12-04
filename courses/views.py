from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson


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


# Optional: Login-required view example
@login_required
def my_courses(request):
    """Show courses for logged-in users"""
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'courses/my_courses.html', {'courses': courses})