from django import forms
from .models import Groups, Notes


class GroupsForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = '__all__'
        exclude = ['order']


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = '__all__'
        exclude = ['user', 'created', 'modifed', 'name_modifed']
