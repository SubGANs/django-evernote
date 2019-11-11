from django.shortcuts import render
from django.db.models import Q
from notes.models import Notes
import operator

from users_notes.models import UserNotes
from django.contrib.auth.decorators import login_required
from functools import reduce


# Поиск
@login_required
def search(request):
    # поиск на главной панели, методом POST, потому что без условий, ищет везде
    if request.method == 'POST':
        text = request.POST.get('text', '')

        # если отправили пустой запрос
        if len(text) == 0:
            return render(request, 'search-result.html', {'notes': None})

        # если не пустой запрос, делим запрос на слова и для каждого создаем запрос в БД
        if len(text) != 0:
            text = text.split()
            criterions = []
            for word in text:
                criterions.append(Q(head__icontains=word) | Q(body__icontains=word) |
                                  Q(tags_choices__tag__icontains=word))
            result = Notes.objects.filter(reduce(operator.and_, criterions)).filter(public=True).distinct()

            return render(request, 'search-result.html', {'notes_public': result,
                                                          'text': request.POST.get('text', '')})

    # GET запрос в поиске, расширенный поиск
    elif request.method == 'GET':
        text = request.GET.get('text', '')

        # если отправили пустой запрос, то просто возвращаем пустой результат
        if len(text) == 0:
            return render(request, 'search-result.html', {'notes': None})

        # получаем статусы переключателей
        head = ('head', request.GET.get('head'))
        body = ('body', request.GET.get('body'))
        tags = ('tags_choices__tag', request.GET.get('tags'))

        # если запрос не пустой, делим на слова
        if len(text) != 0:
            text = text.split()

            # Поиск по публичным заметкам
            result_public = Notes.objects.none()
            # проходимся по переключателям и их статусам и создаем запрос, далее его собираем в один
            criterions = []
            for word in text:
                filter_search = Q()
                for name, state in head, body, tags:
                    if state == 'on':
                        q = ('%s__icontains' % name, word)
                        filter_search = filter_search | Q(q)
                # Если в публичном поиске нужно искать, то добавляем в фильтр
                if filter_search:
                    criterions.append(filter_search)

            if criterions:
                result_public = Notes.objects.filter(reduce(operator.and_, criterions)).filter(public=True).distinct()

            # Поиск по личным заметкам
            result_private = UserNotes.objects.none()
            if request.GET.get('private'):
                criterions = []
                for word in text:
                    criterions.append(Q(head__icontains=word) |
                                      Q(body__icontains=word) |
                                      Q(tags__icontains=word))
                result_private = UserNotes.objects.filter(reduce(operator.and_, criterions)).filter(user=request.user).distinct()

            return render(request, 'search-result.html', {'notes_public': result_public,
                                                          'notes_private': result_private,
                                                          'text': request.GET.get('text', '')})
