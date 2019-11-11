from django.contrib import admin
from martor.widgets import AdminMartorWidget

from .models import UserGroups, UserNotes


class UserGroupsAdmin(admin.ModelAdmin):
    models = UserGroups
    list_display = ('name', 'user',)


class UserNotesAdmin(admin.ModelAdmin):
    models = UserNotes
    list_display = ('head', 'user', 'group', 'created',)
    list_filter = ('created',)
    formfield_overrides = {
        models.body: {'widget': AdminMartorWidget},
    }


admin.site.register(UserGroups, UserGroupsAdmin)
admin.site.register(UserNotes, UserNotesAdmin)
