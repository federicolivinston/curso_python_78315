# Generated by Django 5.2.4 on 2025-07-21 15:12

import django.core.files.storage
import django.db.models.deletion
import library.models
import pathlib
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_alter_book_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='user_booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books_reserved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/media/', location=pathlib.PureWindowsPath('C:/Users/ADMIN/Desktop/cursos/python_78315/entregas/entrega_final/curso_python_78315/book_library/media')), upload_to=library.models.book_image_upload_to),
        ),
    ]
