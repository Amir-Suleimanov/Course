# Generated by Django 4.2 on 2024-09-08 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_certificate_options_alter_notification_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='post',
            field=models.CharField(choices=[('ST', 'Student'), ('TR', 'Teacher')], default='ST', max_length=2),
        ),
    ]
