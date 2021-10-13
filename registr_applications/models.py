from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


def user_directory_path(instance, filename):
    """директория для сохранения документов пользователя"""
    return "docs\\user_{}_{}/{}".format(instance.user.id, instance.user, filename)


class Statement(models.Model):
    """Модель Заявление"""
    number = models.AutoField(primary_key=True, verbose_name='уникальный номер')
    name = models.CharField(max_length=300,  verbose_name='наименование услуги')
    content = models.TextField(max_length=10000, null=True, verbose_name='текст заявления')
    date = models.DateTimeField(auto_now=True, blank=True, verbose_name='дата подачи')
    status = models.CharField(max_length=300, blank=True, db_index=True, verbose_name='статус')
    result = models.CharField(max_length=400, verbose_name='Результат')
    email = models.CharField(max_length=400,  verbose_name='Почтовый адрес')
    passed = models.BooleanField(default=False)   #было ли рассмотрено админом
    # Админ последним внесший изменения
    admin = models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE, related_name='admin_set', verbose_name='Специалист')
    # Пользователь создавший заявление
    user = models.ForeignKey(User, blank=True,null=True, on_delete=models.CASCADE, related_name='user_set', verbose_name='Пользователь')
    # docs = models.ImageField(upload_to="docs\\"+ str(users), verbose_name='Image')
    docs = models.ImageField(upload_to=user_directory_path, null=True, )

    def get_absolute_url(self):
        return '/'

    def __str__(self):
        return str(self.number) + self.name

# Create your models here.
