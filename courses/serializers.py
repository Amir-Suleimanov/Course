from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.validators import ValidationError
from django.db.models import Max

from courses.models import Course, Lesson, Purchase


class EmptySerializer(Serializer):
    pass


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'author', 'lessons', 'price']
        extra_kwargs = {
            'author': {'read_only': True},
            'lessons': {'read_only': True},
        }


    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['author'] = request.user
        else:
            raise ValidationError('Пользователь должен быть аутентифицирован для создания курса.')
        
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super(CourseSerializer, self).to_representation(instance)
        request = self.context.get('request')
        bought = Purchase.objects.filter(student=request.user, course=instance).exists()
        representation['bought'] = bought
        return representation
    

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'course', 'materials', 'priority', 'assignments',]
        extra_kwargs = {
            'course': {'read_only': True},
            'materials': {'read_only': True},
            'priority': {'read_only': True},
            'assignments': {'read_only': True},
        }
        
    def validate_priority(self, value):
        if value < 1:
            raise ValidationError("Приоритет должен быть положительным числом больше или равным 1.")
        return value
    
    def create(self, validated_data):
        course_id = self.context['course_id']
       
        last_priority = Lesson.objects.filter(course=course_id).aggregate(max_priority=Max('priority'))['max_priority'] or 0
        validated_data['priority'] = last_priority + 1
        validated_data['course_id'] = course_id
        
        return super().create(validated_data)