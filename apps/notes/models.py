import re

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from martor.models import MartorField

from transliterate import translit, get_available_language_codes


# если пользователь удален, сами заметки останутся
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted', first_name='*пользователь удален*')[0]


class Groups(models.Model):
    name = models.CharField(max_length=150, verbose_name='Назавние группы')
    order = models.IntegerField(null=True, blank=True, default=None, verbose_name='Порядок групп')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'groups'
        verbose_name = 'Группу'
        verbose_name_plural = 'Группы'


class Tags(models.Model):
    tag = models.CharField(max_length=150, verbose_name='Теги')

    def __str__(self):
        return self.tag

    class Meta:
        db_table = 'tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Notes(models.Model):
    def translate_note_name(self, name):
        translate_name = translit(name, 'ru', reversed=True).strip()
        translate_name = re.sub(' ', '_', translate_name).lower()
        translate_name = re.sub(r'\W+', '', translate_name)
        return translate_name


    group = models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name='Группа')
    user = models.ForeignKey(User, null=False, on_delete=models.SET(get_sentinel_user), verbose_name="Автор")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    modifed = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    name_modifed = models.CharField(max_length=150, default='', blank=True, verbose_name='Кто изменил')
    head = models.CharField(max_length=150, unique=True, verbose_name='Заголовок')
    body = MartorField(verbose_name='Тело')
    tags_choices = models.ManyToManyField(Tags, blank=True, default=True, verbose_name='Теги')
    public = models.BooleanField(default=False, blank=True, verbose_name='Опубликовано')
    link = models.CharField(max_length=300, blank=True, default='', verbose_name='Ссылка')

    def __str__(self):
        return self.head

    class Meta:
        db_table = "notes"
        verbose_name = "Заметкa"
        verbose_name_plural = "Заметки"

    def save(self, *args, **kwargs):
        self.link = self.translate_note_name(self.head)
        super(Notes, self).save(*args, **kwargs)
