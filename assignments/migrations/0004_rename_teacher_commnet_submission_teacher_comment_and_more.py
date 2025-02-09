# Generated by Django 4.2 on 2024-09-21 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0003_assignment_final_date_alter_assignment_deadline'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='teacher_commnet',
            new_name='teacher_comment',
        ),
        migrations.AlterField(
            model_name='submission',
            name='send_date',
            field=models.DateTimeField(null=True, verbose_name='Дата отправки'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.TextField(choices=[('CH', 'Проверено'), ('UNCH', 'Не проверено')], default='UNCH', max_length=4, verbose_name='Статус'),
        ),
    ]
