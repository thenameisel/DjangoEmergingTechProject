from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    exclude = ['instructor']
    list_display = ['title', 'instructor', 'created_at', 'lesson_count']
    list_filter = ['created_at', 'instructor']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}  # Auto-fill slug
    
    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = 'Number of Lessons'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(instructor=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.instructor = request.user
        super().save_model(request, obj, form, change)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_published', 'published_date']
    list_filter = ['course', 'is_published', 'published_date']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['order', 'is_published']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(course__instructor=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            if not request.user.is_superuser:
                kwargs["queryset"] = Course.objects.filter(instructor=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.course.instructor != request.user and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.course.instructor != request.user and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
