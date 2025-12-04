from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'created_at', 'lesson_count']
    list_filter = ['created_at', 'instructor']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}  # Auto-fill slug
    
    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = 'Number of Lessons'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_published', 'published_date']
    list_filter = ['course', 'is_published', 'published_date']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['order', 'is_published']