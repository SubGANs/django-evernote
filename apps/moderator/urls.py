from django.urls import path, re_path
from django.contrib import admin
from . import views

urlpatterns = [
    path('notes/', views.control_notes, name='control_notes'),
    re_path(r'^edit/(?P<note_id>\w+)/$', views.note_edit, name='control_note_edit'),
    path('groups/', views.order_group, name='order_group'),
    path('feedback/', views.feedback, name='feedback'),
    path('tags/', views.control_tags, name='control_tags'),
    path('tag/add/', views.tag_add, name='tag_add'),
    re_path(r'^tag/delete/(?P<tag_id>\w+)/$', views.tag_delete, name='tag_delete'),
    path('tag/edit/', views.tag_edit, name='tag_edit'),
    path('_count_notes/', views.count_notes, name='count_notes'),
]