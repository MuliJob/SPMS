# Generated by Django 5.2 on 2025-06-19 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('supervisor', 'Supervisor'), ('lecturer', 'Lecturer'), ('admin', 'Admin')], max_length=20),
        ),
    ]
