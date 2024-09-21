from django.db import models

from users.models import User

class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Преподаватель",
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    
    
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    
    def __str__(self) -> str:
        return self.title
    

class Material(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название материала')
    link = models.CharField(max_length=512, verbose_name='Ссылка на материал', null=True, blank=True)

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'
    

    def __str__(self) -> str:
        return f'{self.title} - {self.link}'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание')
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name='lessons'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    materials = models.ManyToManyField(Material, blank=True)
    priority = models.PositiveIntegerField(verbose_name='Порядок')
    

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    
    def __str__(self) -> str:
        return self.title
    

class Review(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    rating = models.IntegerField(verbose_name='Рейтинг')
    text = models.TextField(verbose_name='Отзыв')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    
    def __str__(self) -> str:
        return f'{self.course.title} - {self.rating}'
    

class Purchase(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Покупатель",
    )
    date_purchased = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
    
    def __str__(self):
        return f'Покупка: {self.user.username} - {self.course.title}'
