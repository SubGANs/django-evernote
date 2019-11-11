import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
# from django.contrib.auth import authenticate
from django.contrib import messages
from users_notes.models import UserNotes
# from django.template.loader import render_to_string
from django.core.cache import cache

from telegram import telealert
from .forms import GroupsForm, NotesForm
from .models import Notes, Groups


# Главная, показывает все открытые публичные заметки
@login_required
def public_notes(request):
    # Get all public notes
    cache_key_notes = 'all_pub_notes'
    notes = cache.get(cache_key_notes)

    if not notes:
        notes = Notes.objects.all().order_by('group', '-created').filter(public=True)
        cache.set(cache_key_notes, notes, 3600)

    # Get groups
    cache_key_groups = 'all_pub_groups'
    groups = cache.get(cache_key_groups)

    if not groups:
        groups = Groups.objects.all().order_by('order')
        cache.set(cache_key_groups, groups, 3600)

    return render(request, 'notes-list.html', {'groups': groups, 'notes': notes})


# Добавление заметки
@login_required
def note_add(request, group_id):
    if request.method == 'POST':
        form = NotesForm(request.POST, initial={'group': group_id})
        if form.is_valid():
            note = form.save(commit=False)
            if request.user.groups.filter(name__in=['Moderators']).exists():
                note.public = True
            note.user_id = request.user.id
            note.save()
            form.save_m2m()
            if request.user.groups.filter(name__in=['Moderators']).exists():
                messages.add_message(request, messages.SUCCESS, 'Заметка создана.')
            else:
                messages.add_message(request, messages.SUCCESS, 'Заметка создана и отправлена на проверку, после одобрения она станет доступна.')
                try:
                    telealert.send_message('*Создана новая заметка!*\n Группа: {group}\n Название: {name}\n Автор: {user}'\
                        .format(group=note.group, name=note.head, user=request.user.last_name + ' ' + request.user.first_name))
                except:
                    pass
            return redirect('index')
    else:
        form = NotesForm(initial={'group': group_id})
    return render(request, 'notes-add.html', {'form': form})


# Редактирование заметки
@login_required
def note_edit(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    is_public = note.public
    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            note_form = form.save(commit=False)
            note_form.name_modifed = request.user.last_name + ' ' + request.user.first_name
            note_form.public = is_public
            note_form.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, 'Заметка изменена.')
            return redirect('index')
    else:
        form = NotesForm(instance=note)
    return render(request, 'notes-edit.html', {'form': form})


# Удаление заметки
@login_required
def note_delete(request, note_id):
    if request.is_ajax():
        note = get_object_or_404(Notes, id=note_id)
        delete_note = Notes.objects.get(id=note_id)
        delete_note.delete()
        messages.add_message(request, messages.SUCCESS, 'Заметка удалена.')
        response = {'success': True}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseForbidden('Неверный метод запроса')


# Добавление группы
@login_required
def group_add(request):
    if request.method == 'POST' and request.is_ajax():
        name = request.POST.get('name')
        add_group = Groups(name=name)
        add_group.save()
        response = {'success': True}
        return HttpResponse(json.dumps(response), content_type='application/json')
    elif request.method == 'POST':
        name = request.POST.get('name')
        add_group = Groups(name=name)
        add_group.save()
        return redirect('index')
    return redirect('index')


# Изменение группы
@login_required
def group_edit(request, group_id):
    group = get_object_or_404(Groups, id=group_id)
    if request.method == 'POST':
        form = GroupsForm(request.POST, instance=group)
        if form.is_valid():
            group_form = form.save(commit=False)
            group_form.save()
            messages.add_message(request, messages.SUCCESS, 'Группа изменена.')
            return redirect('index')
    else:
        form = GroupsForm(instance=group)
    return render(request, 'group-edit.html', {'form': form})


# Удаление группы
@login_required
def group_delete(request, group_id):
    if request.is_ajax():
        group = get_object_or_404(Groups, id=group_id)
        delete_group = Groups.objects.get(id=group_id)
        delete_group.delete()
        messages.add_message(request, messages.SUCCESS, 'Группа удалена.')
        response = {'success': True}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseForbidden('Неверный метод запроса')


# Показать расшаренную заметку
def note_view(request, note_link):
    try:
        note = get_object_or_404(Notes, link=note_link)
    except:
        note = get_object_or_404(UserNotes, link=note_link)
    return render(request, 'view-note.html', {'note': note})


@login_required
def note_new(request):
    notes = Notes.objects.all().order_by('-created').filter(public=True)[:20]
    return render(request, 'notes-new.html', {'notes': notes})
