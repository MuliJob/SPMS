# Generated by Django 5.2 on 2025-05-16 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_rename_user_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='supervisor',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
