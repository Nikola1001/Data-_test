from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import StatementUserForm
from django.views.generic import CreateView
from .models import Statement
from django.conf import settings
from django.core.mail import send_mail


def index(request):
    """Корневая страница"""
    return render(request, 'index.html')


class SignUpView(generic.CreateView):
    """Регистрация"""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class StatementCreateView(CreateView):
    """Создание заявления пользователем через форму"""
    template_name = 'create_statement_for_user.html'
    form_class = StatementUserForm
    success_url = '/'


def create_statment_user(request):
    """обработка создания заявления"""
    error=""
    if request.method == 'POST':
        form = StatementUserForm(request.POST, request.FILES)
        if form.is_valid():
            form_ext = form.save(commit=False)
            form_ext.user = request.user
            form_ext.status = "Зарегистрировано"
            form_ext.save()
            # img_obj = form.instance
            return render(request, 'index.html', {"form": form})
        else:
            error = 'Ошибка заполнения формы'
    else:
        form = StatementUserForm()
        data = {
            'form': form,
            "error": error
        }
    return render(request, 'create_statement_for_user.html', data)


def about_stat(request, st_number):
    """информация по заявлению для юзера"""
    stat = Statement.objects.get(number=st_number)
    return render(request, 'about_stat.html', {"stat": stat})


def accept_stat(request, st_number):
    """Обработка заявления"""
    try:
        stat = Statement.objects.get(number=st_number)
        if request.method == "POST":
            stat.content = request.POST.get("content")
            stat.name = request.POST.get("name")
            stat.result = request.POST.get("result")
            # stat.docs = request.POST.get("docs")
            stat.passed = True
            stat.status = request.POST.get("status")
            stat.email = request.POST.get("email")
            stat.admin = request.user
            stat.save()
            try:
                send_mail('Информация о поданном заявлении', 'Изменилися текущий статус заявления \n подробнее в личном кабинете', settings.EMAIL_HOST_USER, ['kolagolikov@yandex.ru'])
            except Exception as ex:
                print(ex)
                print("Не удалось отправить сообщение")
            return HttpResponseRedirect("/")
        else:
            return render(request, "accept_stat.html", {"stat": stat})
    except Statement.DoesNotExist:
        return HttpResponseNotFound("<h2>Заявление не найдено</h2>")


def unprocessed_stat(request):
    """Необработанные заявления"""
    stats = Statement.objects.filter(passed=False)
    return render(request, 'unprocessed.html', {"stats": stats})


def delete_stat(request, st_number):
    """Удаление заявления"""
    try:
        stat = Statement.objects.get(number=st_number)
        # if stat.status = "Отказ"
        stat.delete()
        return HttpResponseRedirect("/")
        # else:
        # return HttpResponseNotFound("<h2>Вы не можете удалить заявление, так как статус не "Отказ"</h2>")
    except Statement.DoesNotExist:
        return HttpResponseNotFound("<h2>Заявление не найдено</h2>")


def my_statements(request):
    """Мои заявления и для юзера и для админа"""
    user = request.user
    if user.is_staff:
        stats = Statement.objects.filter(admin=user)
    else:
        stats = Statement.objects.filter(user=user)
    return render(request, 'my_statements.html', {"stats": stats})


def all_statements(request):
    """Все заявления"""
    stats = Statement.objects.all()
    return render(request, 'all_statements.html', {"stats": stats})


