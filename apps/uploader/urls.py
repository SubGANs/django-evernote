from django.urls import path
from . import views


urlpatterns = [
    # урлы на личные заметки и группы
    path('', views.markdown_uploader, name='uploader'),
]
