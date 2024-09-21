from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from courses.views import (
    CoursesView,
    CourseView, 
    LessonsView, 
    LessonView
    )


app_name = 'courses'

router = SimpleRouter()
router.register(r"", CoursesView, basename='courses')
router.register(r'', CourseView, basename='course')

courses_router = NestedSimpleRouter(router, r'', lookup='course')
courses_router.register(r'lessons', LessonsView, basename='course-lessons')
courses_router.register(r'lessons', LessonView, basename='course-lesson')


urlpatterns = router.urls + courses_router.urls 