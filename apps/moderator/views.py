from django.shortcuts import render, redirect, get_object_or_404
from notes.models import Notes, Groups, Tags
from notes.forms import GroupsForm, NotesForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from telegram import telealert
import json
from django.http import HttpResponse


@login_required
def control_notes(request):
    notes = Notes.objects.all().order_by('created').filter(public=False)
    return render(request, 'control-notes.html', {'notes': notes})



# Редактирование заметки
@login_required
def note_edit(request, note_id):
    note = get_object_or_404(Notes, id=note_id)
    if request.method == 'POST':
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            note_form = form.save(commit=False)
            #note_form.name_modifed = request.user.last_name + ' ' + request.user.first_name
            note_form.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, 'Заметка опубликована.')
            return redirect('control_notes')
    else:
        form = NotesForm(instance=note)
    return render(request, 'note-edit-moderator.html', {'form': form})


# Форма изменения порядка групп
@login_required
def order_group(request):
    if request.user.groups.filter(name__in=['Moderators']).exists():
        if request.method == 'POST':
            for count, value in enumerate(request.POST):
                if count == 0:
                    continue
                if request.POST.get(value):
                    Groups.objects.filter(id=value).update(order=int(request.POST.get(value)))
            messages.add_message(request, messages.SUCCESS, 'Порядок групп изменен.')
            return redirect('index')
        else:
            groups = Groups.objects.all().order_by('order')
            return render(request, 'order-group.html', {'groups': groups})
    else:
        return HttpResponseForbidden('Вам сюда нельзя')


# Управление тегами
@login_required
def control_tags(request):
    if request.user.groups.filter(name__in=['Moderators']).exists():
        tags = Tags.objects.all()
        return render(request, 'control_tags.html', {'tags': tags})


# Добавление тега
@login_required
def tag_add(request):
    if request.method == 'POST' and request.is_ajax():
        name = request.POST.get('name')
        add_tag = Tags(tag=name)
        add_tag.save()
        response = {'success': True}
        messages.add_message(request, messages.SUCCESS, 'Тег добавлен')
        return HttpResponse(json.dumps(response), content_type='application/json')
    elif request.method == 'POST':
        name = request.POST.get('name')
        add_tag = Tags(tag=name)
        add_tag.save()
        messages.add_message(request, messages.SUCCESS, 'Тег добавлен')
        return redirect('control_tags')
    return redirect('control_tags')

# Удаление тега
@login_required
def tag_delete(request, tag_id):
    if request.is_ajax():
        tag = get_object_or_404(Tags, id=tag_id)
        delete_tag = Tags.objects.get(id=tag_id)
        delete_tag.delete()
        messages.add_message(request, messages.SUCCESS, 'Тег удален.')
        response = {'success': True}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseForbidden('Неверный метод запроса')


# Изменение тега
@login_required
def tag_edit(request):
    if request.method == 'POST' and request.is_ajax():
        name = request.POST.get('name')
        tag_id = request.POST.get('id')
        Tags.objects.filter(id=tag_id).update(tag=name)
        messages.add_message(request, messages.SUCCESS, 'Тег изменен.')
        response = {'success': True}
        return HttpResponse(json.dumps(response), content_type='application/json')
    elif request.method == 'POST':
        name = request.POST.get('name')
        tag_id = request.POST.get('id')
        Tags.objects.filter(id=tag_id).update(tag=name)
        messages.add_message(request, messages.SUCCESS, 'Тег изменен.')
        return redirect('control_tags')
    else:
        return HttpResponseForbidden('Неверный метод запроса')

# Форма обратной связи
@login_required
def feedback(request):
    if request.method == 'POST':
        try:
            text = request.POST.get('text')
            subject = '*NOTES*\n_Сообщение от: {last_name} {first_name}_\n'.format(last_name=request.user.last_name, first_name=request.user.first_name)
            send = telealert.send_me_message(subject + text)
            response = {'success': True}
            messages.add_message(request, messages.SUCCESS, 'Ваше пожелание отправлено.')
            return HttpResponse(json.dumps(response), content_type='application/json')
        except:
            response = {'success': False}
            messages.add_message(request, messages.ERROR, 'Произошла ошибка, попробуйте позже.')
            return HttpResponse(json.dumps(response), content_type='application/json')


# Счетчик заметок
@login_required
def count_notes(request):
    try:
        if request.user.groups.filter(name__in=['Moderators']).exists():
            notes = Notes.objects.all().filter(public=True).count()
            on_public = Notes.objects.all().filter(public=False).count()
            response = {'success': True, 'count': notes, 'on_public': on_public}
        else:
            notes = Notes.objects.all().filter(public=True).count()
            response = {'success': True, 'count': notes}
        return HttpResponse(json.dumps(response), content_type='application/json')
    except:
        response = {'success': False, 'count': '?', 'on_public': '?'}
        return HttpResponse(json.dumps(response), content_type='application/json')