from django.db import models


class Assignment(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False, verbose_name='Название задачи')
    description = models.TextField(blank=False, null=False, verbose_name='Описание задачи')
    lesson = models.ForeignKey(
        'courses.Lesson',
        on_delete=models.CASCADE, 
        related_name='assignments', 
        verbose_name='Урок'
    )
    deadline = models.PositiveIntegerField(blank=False, null=False, verbose_name='Срок сдачи')
    final_date = models.DateTimeField(null=True, verbose_name='День сдачи')


    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
    
    def __str__(self):
        return self.title


class Submission(models.Model):

    class STATUS(models.TextChoices):
        checked = ('CH', 'Проверено')
        unchecked = ('UNCH', 'Не проверено')


    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Студент'
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Задание'
    )
    answer = models.TextField(verbose_name='Ответ')
    status = models.TextField(max_length=4, choices=STATUS.choices, default=STATUS.unchecked, verbose_name='Статус')
    teacher_comment = models.TextField(verbose_name='Комментарии преподавателя')
    send_date = models.DateTimeField(null=True, verbose_name='Дата отправки')


    class Meta:
        verbose_name = 'Отправленное задание'
        verbose_name_plural = 'Отправленные задания'

    def __str__(self):
        return self.assignment.title + " - " + self.student.username


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    lesson = models.ForeignKey(
        'courses.Lesson',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Урок',
        null=True
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Задание',
        null=True
    )
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Ответ к заданию'
    )
    

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text