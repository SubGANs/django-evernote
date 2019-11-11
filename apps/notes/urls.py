from django.urls import path, re_path
from notes import views


urlpatterns = [
    # урлы на публичные заметки и группы
    re_path(r'^add/(?P<group_id>\w+)/$', views.note_add, name='note_add'),
    re_path(r'^note/edit/(?P<note_id>\w+)/$', views.note_edit, name='note_edit'),
    re_path(r'^note/delete/(?P<note_id>\w+)/$', views.note_delete, name='note_delete'),
    path('group/add/', views.group_add, name='group_add'),
    re_path(r'^group/delete/(?P<group_id>\w+)/$', views.group_delete, name='group_delete'),
    re_path(r'^group/edit/(?P<group_id>\w+)/$', views.group_edit, name='group_edit'),
    re_path(r'^view/(?P<note_link>\w+)/$', views.note_view, name="note_view"),
    path('new/', views.note_new, name="note_new"),
]
