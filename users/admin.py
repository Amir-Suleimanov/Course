from django.contrib import admin

from users.models import Balance, User, Certificate, Notification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'post', 'date_registration', 'balance']
    filter_horizontal = ['courses']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'date_obtained', 'status']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'date_created', 'is_read']


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ['owner', 'amount']