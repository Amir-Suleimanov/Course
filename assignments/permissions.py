from rest_framework.permissions import BasePermission, SAFE_METHODS

from courses.models import Course

class AssignmentsPermission(BasePermission):
    message = 'Только студенты могут создавать задания'
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            self.message = 'Пользователь должен быть авторизованным'
            return False
        
        if request.method in SAFE_METHODS:
            if not request.method == 'GET':
                return True

            course_id = view.kwargs['course_pk']
            try:
                if request.user in Course.objects.get(id=course_id).students.all():
                    return True
                self.message = 'Вы не являетесь студентом данного курса'
                return False
            except Course.DoesNotExist:
                self.message = 'Курс не найден'
                return False

        if request.method == 'POST':
            if request.user.is_staff:
                return True
            
            course_id = view.kwargs['course_pk']
            course = Course.objects.get(id=course_id)

            if request.user is course.author:
                return True

        return False
        

class AssignmentPermission(BasePermission):
    message = 'У вас нет прав чтобы просматривать данное задание'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            self.message = 'Пользователь должен быть авторизованным'
            return False

        if request.method in SAFE_METHODS:
            if not request.method == 'GET':
                return True

            course_id = view.kwargs['course_pk']
            try:
                if request.user in Course.objects.get(id=course_id).students.all():
                    return True
                self.message = 'Вы не являетесь студентом данного курса'
                return False
            except Course.DoesNotExist:
                self.message = 'Курс не найден'
                return False
        
        if request.method == 'PUT' or request.method == 'DELETE':
            course_id = view.kwargs['course_pk']
            
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                self.message = 'Курс не найден'
                return False
            
            if request.user == course.author:
                return True
            
            self.message = "У вас нет прав на изменение данного задания"
            return False

        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            self.message = 'Пользователь должен быть авторизованным'
            return False
    
        if request.method in ('PUT', 'DELETE') and request.user.post == 'TR':
            return obj.lesson.course.author == request.user
        
        return True
    

class SubmissionsPermission(BasePermission):
    message = 'У вас нет прав чтобы просматривать ответы на задания'
    
    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            self.message = 'Пользователь должен быть авторизованным'
            return False
        
        if request.method in SAFE_METHODS:
            course_pk = view.kwargs['course_pk']
            
            try:
                course = Course.objects.get(id=course_pk)
            except Course.DoesNotExist:
                self.message = 'Курс не найден'
                return False
            
            if request.user in course.students.all():
                return True

        if request.method == 'POST':
            course_id = view.kwargs['course_pk']
            
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                self.message = 'Курс не найден'
                return False
            
            if request.user in course.students.all() or request.user == course.author:
                return True
            
            self.message = "У вас нет прав на изменение данного задания"
            return False

        return False


class SubmissionPermission(BasePermission):
    message = 'У вас недостаточно прав для данного действия'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            self.message = 'Пользователь должен быть авторизованным'
            return False
        
        if request.method in SAFE_METHODS:
            return True

        if request.method in ('PUT', 'DELETE'):
            self.message = 'У вас нет прав для изменения данного ответа'
            return obj.assignment.student == request.user

        return False