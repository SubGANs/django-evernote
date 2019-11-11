from django.urls import path
from . import views


urlpatterns = [
    # Поиск
    path('', views.search, name='search'),
]
