from django.contrib import admin

from assignments.models import Assignment, Submission, Comment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'lesson', 'deadline')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'answer', 'status', 'teacher_comment', 'send_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'lesson', 'text', 'created', 'assignment', 'submission')