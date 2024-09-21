from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action

from courses.models import (
    Course, 
    Lesson
    )
from courses.serializers import (
    CourseSerializer, 
    LessonSerializer,
    EmptySerializer
    )
from courses.permissions import (
    IsTeacherOrReadOnly, 
    LessonsPermisson, 
    LessonPermission, 
    CoursePermission,
    IsNotStudentorNotBalance
    )
from users.models import Balance, User

class CoursesView(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherOrReadOnly]


class CourseView(UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CoursePermission]
    
    @action(
        methods=['POST'],
        detail=True,
        serializer_class=EmptySerializer,
        permission_classes=[IsAuthenticated, IsNotStudentorNotBalance]
    )
    def pay(self, request, pk, *args, **kwargs):
        user: User = request.user
        balance: Balance = user.balance
        course: Course = Course.objects.get(id=pk)
        
        balance.amount -= course.price
        balance.save()
        user.courses.add(course)

        url = reverse(
                viewname='courses:course-detail',
                kwargs={
                    'pk': pk,
                }
            )
        return HttpResponseRedirect(url)


class LessonsView(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, LessonsPermisson]

    def get_queryset(self):
        course_id = self.kwargs['course_pk']
        return Lesson.objects.filter(course_id=course_id)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['course_id'] = self.kwargs['course_pk']
        return context


class LessonView(UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, LessonPermission]

    def get_queryset(self):
        lesson_id = self.kwargs['pk']
        lesson = Lesson.objects.get(id=lesson_id)
        course = Course.objects.get(pk=self.kwargs['course_pk'])
        if not (lesson in course.lessons.all()):
            raise NotFound(detail="Страница не существует", code=404)

        return Lesson.objects.filter(pk=lesson_id)