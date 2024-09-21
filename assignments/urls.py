from rest_framework_nested.routers import NestedSimpleRouter

from assignments.views import (
    AssignmentsView, 
    AssignmentView,
    SubmissionsView, 
    SubmissionView
    )
from courses.urls import courses_router

app_name = 'assignments'

assignment_router = NestedSimpleRouter(courses_router, r'lessons', lookup='lesson')
assignment_router.register(r'assignments', AssignmentsView, basename='assignment-list')
assignment_router.register(r'assignments', AssignmentView, basename='assignment')

submission_router = NestedSimpleRouter(assignment_router, r'assignments', lookup='assignment')
submission_router.register(r'submissions', SubmissionsView, basename='submission-list')
submission_router.register(r'submissions', SubmissionView, basename='submission')

urlpatterns = assignment_router.urls + submission_router.urls