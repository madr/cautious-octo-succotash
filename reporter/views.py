from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from core.models import Project, AbsenceCategory, TajmUser
from reporter.lib import ProgressAbsenceEditForm, _delete_progress, _save_progress, _get_reporter_context, _get_edit_progress_context, \
    ProgressAbsenceForm, _save_absence, _delete_absence


@login_required
def report(request, year=None, week_label=None, day=None):
    user = TajmUser.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = ProgressAbsenceForm(request.POST)
        if form.is_valid():
            absence_saved = _save_absence(user, form)
            return absence_saved if absence_saved else _save_progress(user, form)
        else:
            return render(request, 'reporter.html', _get_reporter_context(form, user, year, week_label, day))
    else:
        return render(request, 'reporter.html', _get_reporter_context(None, user, year, week_label, day))


@login_required
@require_http_methods(['GET'])
def delete_progress(request, progress_id):
    return _delete_progress(progress_id)

@login_required
@require_http_methods(['GET'])
def projects(request):
    projects_and_absences = [p.name for p in Project.objects.filter(active=True)]
    projects_and_absences += [ac.name for ac in AbsenceCategory.objects.filter(active=True)]
    return JsonResponse(projects_and_absences, safe=False)


@login_required
def edit_progress(request, progress_id):
    if request.method == 'POST':
        form = ProgressAbsenceEditForm(request.POST)
        if form.is_valid():
            return _save_progress(request.user, form, progress_id)
        else:
            return render(request, 'edit-progress.html', _get_edit_progress_context(form, progress_id))
    else:
        return render(request, 'edit-progress.html', _get_edit_progress_context(None, progress_id))


@login_required
@require_http_methods(['GET'])
def delete_absence(request, absence_id):
    y, wl, d = _delete_absence(absence_id)
    return redirect('anyday', year=y, week_label=wl, day=d)