from rest_framework.serializers import ModelSerializer, IntegerField
from rest_framework.validators import ValidationError
from rest_framework.decorators import action
# from django.db.models import Max

from assignments.models import Assignment, Submission
from courses.models import Course, Lesson


class AssignmentSerializer(ModelSerializer):
    deadline_hours = IntegerField(required=True, write_only=True, label="Время на выполнение в часах")
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'lesson', 'deadline', 'final_date', 'deadline_hours']
        extra_kwargs = {
            'lesson': {'read_only': True},
            'deadline_hours': {'write_only': True},
            'deadline': {'read_only': True},
            'final_date': {'read_only': True},
        }

    def create(self, validated_data):
        lesson_pk = self.context.get('lesson_id')
        request = self.context.get('request')
        
        if not(lesson_pk and request.user.is_authenticated):
            raise ValidationError('Пользователь должен быть аутентифицирован для создания курса.')
        
        validated_data['lesson'] = Lesson.objects.get(id=lesson_pk)
        validated_data['deadline'] = validated_data.pop('deadline_hours')
        validated_data['final_date'] = None
        
        return super().create(validated_data)
    
    
class SubmissionSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'student', 'assignment', 'answer', 'status', 'teacher_comment', 'send_date']
        # extra_kwargs = {
        #     'student': {'read_only': True},
        #     'assignment': {'read_only': True},
        #     'teacher_comment': {'read_only': True},
        #     'send_date': {'read_only': True},
        #     'status': {'read_only': True},
        # }
    
    # def to_representation(self, instance):
    #     representation = super(CourseSerializer, self).to_representation(instance)
    #     request = self.context.get('request')
    #     bought = Purchase.objects.filter(student=request.user, course=instance).exists()
    #     representation['bought'] = bought
    #     return representation