from django.urls import path

from views import NotificationListCreateView, NotificationView

app_name = 'users'

urlpatterns = [
    path('notifications/', NotificationListCreateView, name='notifications_list'),
    path('notifications/<int:pk>/', NotificationView, name='notification')
]