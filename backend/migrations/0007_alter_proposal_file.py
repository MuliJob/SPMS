# Generated by Django 5.2 on 2025-05-17 06:26

import backend.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_rename_document_proposal_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='file',
            field=models.FileField(upload_to=backend.models.proposal_upload_path),
        ),
    ]
