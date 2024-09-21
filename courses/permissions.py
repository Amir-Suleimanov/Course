from rest_framework.permissions import SAFE_METHODS, BasePermission

from courses.models import Course


class IsTeacherOrReadOnly(BasePermission):
    message = 'Только преподаватели могут создавать курс'

    def has_permission(self, request, view):
        
        if not request.user.is_authenticated:
            self.message = 'Пользователь должен быть авторизованным'
            return False
        
        if request.method == 'POST':
            return request.user.post == 'TR'
        
        if request.method in SAFE_METHODS:
            return True
        
        return False
    

class CoursePermission(BasePermission):
    message = 'Только перподаватель имеет право менять курс'
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            self.message = 'Пользователь должен быть авторизованным'
            return False
        
        if request.method == 'PUT' or request.method == 'DELETE':
            course_id = view.kwargs.get('pk')
            
            if not course_id:
                return False

            try:
                course = Course.objects.get(pk=course_id)
            except Course.DoesNotExist:
                self.message = 'Курс не найден'
                return False 
            
            if course.author == request.user or request.user.is_staff:
                return True
            
            return False
        
        if request.method in SAFE_METHODS:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            self.message = 'Пользователь должен быть авторизованным'
            return False
        
        if request.method in ('PUT', 'DELETE') and request.user.post == 'TR':
            return obj.author == request.user
        
        return True
    
    
class LessonsPermisson(BasePermission):
    '''Только администраторы и учителя могут создавать уроки, и только студенты могут их просматривать'''

    message = 'Только администраторы и учителя могут создавать уроки, и только студенты могут их просматривать'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            self.message = 'Пользователь должен быть авторизованным'
            return False

        if request.method in SAFE_METHODS:
            if not request.method == 'GET':
                return True

            course_id = view.kwargs['course_pk']
            try:
                if request.user in Course.objects.get(id=course_id).students.all() :
                    return True
                self.message = 'Курс не был приобретён пользователем'
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


class LessonPermission(BasePermission):
    message = 'Только преподаватели могут изменять урок'

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
            if request.user == course.author:
                return True
            
            return False
        
        return False

    def has_object_permission(self, request, view, obj):
        message = 'Только преподаватели могут изменять урок'
        if not request.user.is_authenticated:
            self.message = 'Пользователь должен быть авторизованным'
            return False
    
        if request.method in ('PUT', 'DELETE') and request.user.post == 'TR':
            return obj.course.author == request.user
        
        return True
    
class IsNotStudentorNotBalance(BasePermission):
    message = 'Вы уже купили данный курс'
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if not request.user.is_authenticated:
            self.message = 'Пользователь должен быть авторизованным'
            return False
        if request.user.is_staff:
            return True
        if request.method == 'POST':
            course = Course.objects.get(id=view.kwargs['pk'])
            if course not in request.user.courses.all():
                if request.user.balance.amount < course.price:
                    self.message = 'У вас недостаточно средств на балансе'
                    return False
                return True
        return False


