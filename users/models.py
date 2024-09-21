from django.db import models
from django.contrib.auth.models import AbstractUser


class Balance(models.Model):
    owner = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        null=True,
        blank=True,
        related_name='balance'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=1000, verbose_name='Баланс')

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'


class User(AbstractUser):
    """
    {
        "username": "",
        "email": "",
        "password": "",
        "password2": ""
    }
    """
    class POST(models.TextChoices):
        STUDENT = ('ST', 'Student')
        TEACHER = ('TR', 'Teacher')
        

    email = models.EmailField(max_length=255, unique=True, null=False, blank=False, verbose_name='Email')
    post = models.CharField(max_length=2, choices=POST.choices, default=POST.STUDENT)
    date_registration = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')
    courses = models.ManyToManyField(
        'courses.course', 
        blank=True, 
        verbose_name='Купленные курсы',
        related_name='students'
        )


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return self.username    


class Certificate(models.Model):
    user = models.ForeignKey(
        User, 
        related_name='Сертификаты',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        'courses.Course',
        related_name='Сертификаты',
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )
    date_obtained = models.DateField(null=False, blank=False, verbose_name='Дата получения сертификата', auto_created=True)
    status = models.BooleanField(default=False, verbose_name='Статус')


    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'


    def __str__(self):
        return f'Сертификат {self.user.username} на курс {self.course.title}'


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        related_name='Уведомления',
        on_delete=models.CASCADE,
        verbose_name='Получатель'
    )
    message = models.TextField(verbose_name='Сообщение')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    date_created = models.DateTimeField(null=False, blank=False, verbose_name='Дата создания уведомления', auto_now_add=True)


    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
    

    def __str__(self):
        return f'Уведомление для {self.user.username}'
    



