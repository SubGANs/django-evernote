from django import forms

from .models import UserGroups, UserNotes


class UserGroupsForm(forms.ModelForm):
    class Meta:
        model = UserGroups
        fields = '__all__'
        exclude = ['user', 'order']


class UserNotesForm(forms.ModelForm):
    tags = forms.CharField(label='Теги', required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Введите список тегов через запятую'}))

    class Meta:
        model = UserNotes
        fields = '__all__'
        exclude = ['user', 'created', 'modifed']

    def __init__(self, user, *args, **kwargs):
        super(UserNotesForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = UserGroups.objects.filter(user_id=user)
