# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from core.lib import TimeUtil
from legacy.lib import ProgressEditForm, _delete_progress, _save_progress, _get_home_context, _get_edit_progress_context, _get_projects_context, ProgressForm, \
    AbsenceForm, _delete_absence


@login_required
def report(request, year=None, week_label=None, day=None):
    if request.method == 'POST':
        form = ProgressForm(request.POST)

        if form.is_valid():
            return _save_progress(request.user, form)
        else:
            context = _get_home_context(form, request.user, year, week_label, day)

            return render(request, 'home.html', context)
    else:
        context = _get_home_context(None, request.user, year, week_label, day)

        return render(request, 'home.html', context)


@login_required
@require_http_methods(['GET'])
def delete_progress(request, year, week_label, day, progress_id):
    _delete_progress(progress_id)

    return redirect('anyday', year=year, week_label=week_label, day=day)


@login_required
@require_http_methods(['GET'])
def projects(request):
    context = _get_projects_context()

    t = loader.get_template('projects.html')
    
    return HttpResponse(t.render(context), content_type='text/javascript')


@login_required
def edit_progress(request, year, week_label, day, progress_id):
    if request.method == 'POST':
        form = ProgressEditForm(request.POST)

        if form.is_valid():
            return _save_progress(request.user, form, progress_id)
        else:
            context = _get_edit_progress_context(form, year, week_label, day, progress_id)
            return render(request, 'edit-progress.html', context)
    else:
        context = _get_edit_progress_context(None, year, week_label, day, progress_id)
        return render(request, 'edit-progress.html', context)


@login_required
@require_http_methods(['POST'])
def add_absence(request):
    form = AbsenceForm(request.POST, initial={'user': request.user})

    if form.is_valid():
        form.save()

    y, wl, d = TimeUtil.ywd(form.cleaned_data['done_at']).split('-')

    return redirect('anyday', year=y, week_label=wl, day=d)


@login_required
@require_http_methods(['GET'])
def delete_absence(request, absence_id):
    y, wl, d = _delete_absence(absence_id)
    return redirect('anyday', year=y, week_label=wl, day=d)


@login_required
@require_http_methods(['GET', 'POST'])
def edit_absence(request, absence_id):


    return redirect('home')
