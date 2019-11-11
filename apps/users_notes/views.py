import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages

from notes.models import Notes
from .models import UserGroups, UserNotes
from .forms import UserGroupsForm, UserNotesForm


# Управление личными заметками
@login_required
def user_notes(request):
    groups = UserGroups.objects.all().filter(user_id=request.user.id).order_by('order')
    notes = UserNotes.objects.all().order_by('group', '-created').filter(user_id=request.user.id)
    return render(request, 'notes-list-user.html', {'groups': groups, 'notes': notes})


# Добавление заметки
@login_required
def user_note_add(request, group_id):
    if request.method == 'POST':
        form = UserNotesForm(request.user, request.POST, initial={'group': group_id})
        if form.is_valid():
            note = form.save(commit=False)
            note.user_id = request.user.id
            note.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, 'Заметка создана.')
            return redirect('user_note')
    else:
        form = UserNotesForm(request.user, initial={'group': group_id})
    return render(request, 'notes-add-user.html', {'form': form})


# Редактирование заметки
@login_required
def user_note_edit(request, note_id):
    note = get_object_or_404(UserNotes, id=note_id)
    if request.method == 'POST':
        form = UserNotesForm(request.user, request.POST, instance=note)
        if form.is_valid():
            note_form = form.save(commit=False)
            note_form.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, 'Заметка изменена.')
            return redirect('user_note')
    else:
        form = UserNotesForm(request.user, instance=note)
    return render(request, 'notes-edit-user.html', {'form': form})


# Удаление заметки
@login_required
def user_note_delete(request, note_id):
    if request.is_ajax():
        note = get_object_or_404(UserNotes, id=note_id)
        delete_note = UserNotes.objects.get(id=note_id)
        delete_note.delete()
        messages.add_message(request, messages.SUCCESS, 'Заметка удалена.')
        response = {'success': True}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseForbidden('Неверный метод запроса')


# Добавление группы
@login_required
def user_group_add(request):
    print(request)
    if request.method == 'POST' and request.is_ajax():
        name = request.POST.get('name')
        add_group = UserGroups(name=name)
        add_group.user_id = request.user.id
        add_group.save()
        response = {'success': True}
        return HttpResponse(json.dumps(response), content_type='application/json')
    elif request.method == 'POST':
        name = request.POST.get('name')
        add_group = UserGroups(name=name)
        add_group.user_id = request.user.id
        add_group.save()
        return redirect('user_note')
    return redirect('user_note')


# Изменение группы
@login_required
def user_group_edit(request, group_id):
    group = get_object_or_404(UserGroups, id=group_id)
    if request.method == 'POST':
        form = UserGroupsForm(request.POST, instance=group)
        if form.is_valid():
            group_form = form.save(commit=False)
            group_form.save()
            messages.add_message(request, messages.SUCCESS, 'Группа изменена.')
            return redirect('user_note')
    else:
        form = UserGroupsForm(instance=group)
    return render(request, 'group-edit-user.html', {'form': form})


# Удаление группы
@login_required
def user_group_delete(request, group_id):
    if request.is_ajax():
        group = get_object_or_404(UserGroups, id=group_id)
        delete_group = UserGroups.objects.get(id=group_id)
        delete_group.delete()
        messages.add_message(request, messages.SUCCESS, 'Группа удалена.')
        response = {'success': True}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseForbidden('Неверный метод запроса')


# Форма изменения порядка групп
@login_required
def order_group(request):
    if request.method == 'POST':
        for count, value in enumerate(request.POST):
            if count == 0:
                continue
            if request.POST.get(value):
                UserGroups.objects.filter(id=value, user_id=request.user).update(order=int(request.POST.get(value)))
        messages.add_message(request, messages.SUCCESS, 'Порядок групп изменен.')
        return redirect('user_note')
    else:
        groups = UserGroups.objects.filter(user_id=request.user).order_by('order')
        return render(request, 'order-group-user.html', {'groups': groups})


@login_required
def user_published_notes(request):
    notes = Notes.objects.all().order_by('-created').filter(user_id=request.user.id, public=True)
    return render(request, 'notes-list-published.html', {'notes': notes})


@login_required
def user_unpublished_notes(request):
    notes = Notes.objects.all().order_by('-created').filter(user_id=request.user.id, public=False)
    return render(request, 'notes-list-unpublished.html', {'notes': notes})
