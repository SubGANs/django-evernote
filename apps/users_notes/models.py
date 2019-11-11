import re
import random
import string

from django.db import models
from martor.models import MartorField
from django.contrib.auth.models import User

from transliterate import translit, get_available_language_codes


class UserGroups(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=150, verbose_name='Назавние группы')
    order = models.IntegerField(null=True, blank=True, default=None, verbose_name='Порядок групп')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user_groups'
        verbose_name = 'Пользовательскую группу'
        verbose_name_plural = 'Пользовательские группы'


class UserNotes(models.Model):
    def translate_note_name(self, name):
        translate_name = translit(name, 'ru', reversed=True).strip()
        translate_name = re.sub(' ', '_', translate_name).lower()
        translate_name = re.sub(r'\W+', '', translate_name)
        return translate_name

    group = models.ForeignKey(UserGroups, on_delete=models.CASCADE, verbose_name='Группа')
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, verbose_name="Автор")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    modifed = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    head = models.CharField(max_length=150, verbose_name='Заголовок')
    body = MartorField(verbose_name='Тело')
    tags = models.CharField(max_length=300, blank=True, default='', verbose_name='Теги')
    link = models.CharField(max_length=300, blank=True, default='', verbose_name='Ссылка')

    def __str__(self):
        return self.head

    class Meta:
        db_table = "user_notes"
        verbose_name = "Пользовательскую заметку"
        verbose_name_plural = "Пользовательские заметки"

    def save(self, *args, **kwargs):
        random_str = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(5)]).lower()
        self.link = self.translate_note_name(self.head) + '_' + random_str
        super(UserNotes, self).save(*args, **kwargs)
