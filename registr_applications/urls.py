from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add_statement/', create_statment_user, name='add_statement'),
    path('my_statements/', my_statements, name='my_statements'),
    path('about_stat/<int:st_number>', about_stat, name='about_stat'),
    path('accept_stat/<int:st_number>', accept_stat, name='accept_stat'),
    path('unprocessed/', unprocessed_stat, name='unprocessed_stat'),
    path('delete_stat/<int:st_number>', delete_stat, name='delete_stat'),
    path('all_statements/', all_statements, name='all_statements'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)