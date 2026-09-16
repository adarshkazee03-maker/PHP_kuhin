"""
Migration: make resources_resource.file nullable.
This fixes the IntegrityError: NOT NULL constraint failed: resources_resource.file
that occurred when submitting link-type resources with no file upload.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='file',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to='resources/files/',
                help_text='Optional file upload (PDF, DOCX, etc.)',
            ),
        ),
        migrations.AlterField(
            model_name='resource',
            name='thumbnail',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='resources/thumbnails/',
            ),
        ),
    ]
