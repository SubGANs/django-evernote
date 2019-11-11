from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from notes import views as main_views

urlpatterns = [
    path('notesadmin/', admin.site.urls),
    re_path(r'^accounts/', include('allauth.urls')),
    path('martor/', include('martor.urls')),
    path('', main_views.public_notes, name='index'),
    path('', include('notes.urls')),
    path('my/', include('users_notes.urls')),
    path('control/', include('moderator.urls')),
    path('search/', include('search.urls')),
    path('uploader/', include('uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
