from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add_statement/', StatementCreateView.as_view(), name='add_statement'),
    path('my_statements/', MyStatsList.as_view(), name='my_statements'),
    path('about_stat/<int:pk>', StatDetailView.as_view(), name='about_stat'),
    path('accept_stat/<int:pk>', StatUpdateView.as_view(), name='accept_stat'),
    path('unprocessed/', UnprocessedStatList.as_view(), name='unprocessed_stat'),
    path('delete_stat/<int:st_number>', delete_stat, name='delete_stat'),
    path('all_statements/', AllStatementsList.as_view(), name='all_statements'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)