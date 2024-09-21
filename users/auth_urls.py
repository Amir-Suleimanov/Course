from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView, TokenViewBase

from users.views import RegisterAPIView, LoginAPIView, LogoutAPIView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    # path('token/', TokenViewBase.as_view(), name='token'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]