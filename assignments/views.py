from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin
    )
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.validators import ValidationError
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from django.http import HttpResponseRedirect

from assignments.models import Assignment, Submission
from assignments.serializers import AssignmentSerializer, SubmissionSerializer
from assignments.permissions import (
    AssignmentsPermission, 
    AssignmentPermission,
    SubmissionsPermission,
    SubmissionPermission
    )
from courses.models import Course, Lesson


class AssignmentsView(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, AssignmentsPermission]

    def get_queryset(self):
        lesson_id = self.kwargs['lesson_pk']
        return Assignment.objects.filter(lesson=lesson_id)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lesson_id'] = self.kwargs['lesson_pk']
        return context


class AssignmentView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, AssignmentPermission]

    def get_queryset(self):
        course_pk = self.kwargs['course_pk']
        lesson_pk = self.kwargs['lesson_pk']
        assignment_pk = self.kwargs['pk']  

        try:
            course = Course.objects.get(pk=course_pk)
            lesson = Lesson.objects.get(pk=lesson_pk, course=course)
            assignment = Assignment.objects.get(pk=assignment_pk, lesson=lesson)
        except Course.DoesNotExist:
            raise NotFound(detail="Курс не существует", code=404)
        except Lesson.DoesNotExist:
            raise NotFound(detail="Урок не существует в указанном курсе", code=404)
        except Assignment.DoesNotExist:
            raise NotFound(detail="Задание не существует для указанного урока", code=404)

        return Assignment.objects.filter(pk=assignment_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['course_pk'] = self.kwargs['course_pk']
        return context
    

    @action(
        methods = [
            'GET',
        ],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def start(self, request, course_pk, lesson_pk, pk):
        course = Course.objects.get(id=course_pk)
        
        if not request.user in course.students.all():
            raise ValidationError('Пользователь должен быть учащимся курса для начала выполнения задания.')
        
        assignment: Assignment = self.get_object()
        assignment.final_date = datetime.now()+timedelta(hours=assignment.deadline)
        assignment.save()
        
        assignment_url = reverse(
        viewname='assignments:assignment-detail',
            kwargs={
                'course_pk': course_pk,
                'lesson_pk': lesson_pk,
                'pk': assignment.pk
            }
        )
        return HttpResponseRedirect(assignment_url)
    

class SubmissionsView(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, SubmissionsPermission]

    def get_queryset(self):
        assignment_id = self.kwargs['assignment_pk']
        return Submission.objects.filter(assignment=assignment_id)

class SubmissionView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated, SubmissionPermission]

    def get_queryset(self):
        return Submission.objects.filter(id=self.kwargs['pk'])