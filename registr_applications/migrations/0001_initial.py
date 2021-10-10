# Generated by Django 3.2.8 on 2021-10-10 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import registr_applications.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False, verbose_name='уникальный номер')),
                ('name', models.CharField(max_length=300, verbose_name='наименование услуги')),
                ('content', models.TextField(max_length=10000, null=True, verbose_name='текст заявления')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='дата подачи')),
                ('status', models.CharField(blank=True, db_index=True, max_length=300, verbose_name='статус')),
                ('result', models.CharField(max_length=400, verbose_name='Результат')),
                ('email', models.CharField(max_length=400, verbose_name='Почтовый адрес')),
                ('passed', models.BooleanField(default=False)),
                ('docs', models.ImageField(null=True, upload_to=registr_applications.models.user_directory_path)),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_set', to=settings.AUTH_USER_MODEL, verbose_name='Специалист')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_set', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
