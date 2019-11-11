from django.urls import path, re_path
from . import views


urlpatterns = [
    # урлы на личные заметки и группы
    path('', views.user_notes, name='user_note'),
    re_path(r'^add/(?P<group_id>\w+)/$', views.user_note_add, name='user_note_add'),
    re_path(r'^edit/(?P<note_id>\w+)/$', views.user_note_edit, name='user_note_edit'),
    re_path(r'^delete/(?P<note_id>\w+)/$', views.user_note_delete, name='user_note_delete'),
    path('group/add/', views.user_group_add, name='user_group_add'),
    re_path(r'^group/delete/(?P<group_id>\w+)/$', views.user_group_delete, name='user_group_delete'),
    re_path(r'^group/edit/(?P<group_id>\w+)/$', views.user_group_edit, name='user_group_edit'),
    path('group/', views.order_group, name='user_order_group'),
    path('published/', views.user_published_notes, name='user_published_notes'),
    path('unpublished/', views.user_unpublished_notes, name='user_unpublished_notes'),
]
