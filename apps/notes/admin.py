from django.contrib import admin
from martor.widgets import AdminMartorWidget
from django.contrib.auth.models import Group
from .models import Notes, Groups, Tags


class TagsAdmin(admin.ModelAdmin):
    models = Tags
    list_display = ('tag',)


class GroupsAdmin(admin.ModelAdmin):
    models = Group
    list_display = ('name', 'order')


class NotesAdmin(admin.ModelAdmin):
    models = Notes
    list_display = ('head', 'user', 'group', 'created', 'modifed', 'public')
    list_filter = ('created',)
    formfield_overrides = {
        models.body: {'widget': AdminMartorWidget},
    }


admin.site.register(Groups, GroupsAdmin)
admin.site.register(Notes, NotesAdmin)
admin.site.register(Tags, TagsAdmin)
