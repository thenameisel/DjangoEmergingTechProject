from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Exists
from .models import Course, Lesson, Subscription, LessonCompletion
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

    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(user=request.user, course=course).exists()
        complete_lessons = LessonCompletion.objects.filter(
            user=request.user,
            lesson=OuterRef('pk')
        )

        lessons = lessons.annotate(is_complete=Exists(complete_lessons))

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_subscribed': is_subscribed
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

#Subscribe to a course
@login_required
def toggle_subscription(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if request.method == "POST":
        subscription = Subscription.objects.filter(user=request.user, course=course)

        if subscription.exists():
            subscription.delete()
        else:
            Subscription.objects.create(user=request.user, course=course)

    
    return redirect('courses:course_detail', slug=slug)


# Get subscribed courses
@login_required
def my_courses(request):
    """Show courses for logged-in users"""
    subscribed_courses = Course.objects.filter(subscribers__user=request.user)
    return render(request, 'courses/my_courses.html', {'courses': subscribed_courses})

@login_required
def mark_read_and_next(request, course_slug, lesson_slug):
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    LessonCompletion.objects.get_or_create(user=request.user, lesson=lesson)

    next_lesson  = Lesson.objects.filter(
        course=lesson.course,
        published_date__gt=lesson.published_date
    ).order_by('published_date').first()

    if next_lesson:
        return redirect('courses:lesson_detail', course_slug=next_lesson.course.slug, lesson_slug=next_lesson.slug)
    else:
        return redirect('courses:course_detail', slug=lesson.course.slug)

