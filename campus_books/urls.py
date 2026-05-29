from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('', include('books.urls', namespace='books')),
    path('', include('users.urls', namespace='users')),
    path('api/', include('books.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
