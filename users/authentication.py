from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser


class CustomAuthBackend(BaseBackend):

    def authenticate(request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(username=username )
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None 
        
    def get_user(request, user_id: int) -> AbstractBaseUser | None:
        user_model = get_user_model()
        try: 
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None