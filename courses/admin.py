from django.contrib import admin

from courses.models import Course, Lesson, Review


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'created', 'students')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'course', 'created', 'priority')
    filter_horizontal = ['materials']


@admin.register(Review) 
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'student', 'course', 'rating', 'created')


