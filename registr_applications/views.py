from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import StatementUserForm
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
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

    def post(self, request, *args, **kwargs):
        form = StatementUserForm(request.POST, request.FILES)
        if form.is_valid():
            form_ext = form.save(commit=False)
            form_ext.user = request.user
            form_ext.status = "Зарегистрировано"
            form_ext.save()
            # img_obj = form.instance
        return render(request, 'index.html', {"form": form})


class StatDetailView(DetailView):
    model = Statement
    template_name = 'about_stat.html'
    context_object_name = "stat"


class StatUpdateView(UpdateView):
    model = Statement
    template_name = 'accept_stat.html'
    fields = '__all__'
    context_object_name = "stat"

    def post(self, request, *args, **kwargs):
        stat = Statement.objects.get(number=self.kwargs['pk'])
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

    def get_object(self):
        return Statement.objects.get(number=self.kwargs['pk'])


class UnprocessedStatList(ListView):
    model = Statement
    template_name = 'unprocessed.html'
    context_object_name = "stats"
    allow_empty = False

    def get_queryset(self):
        return Statement.objects.filter(passed=False)


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


class MyStatsList(ListView):
    model = Statement
    template_name = 'my_statements.html'
    context_object_name = "stats"
    allow_empty = False

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Statement.objects.filter(admin=user)
        else:
            return Statement.objects.filter(user=user)


class AllStatementsList(ListView):
    model = Statement
    template_name = 'all_statements.html'
    context_object_name = "stats"

    def get_queryset(self):
      return Statement.objects.all()

