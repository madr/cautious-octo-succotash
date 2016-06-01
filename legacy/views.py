# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import loader, Context
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from legacy.lib import ProgressEditForm, _delete_progress, _save_progress, _get_home_context, _get_edit_progress_context, _get_projects_context, ProgressForm


@login_required
def report(request, year=None, week_label=None, day=None):
    if request.method == 'POST':
        form = ProgressForm(request.POST)

        if form.is_valid():
            return _save_progress(request.user, request.path, form)
        else:
            context = _get_home_context(form, request.user, year, week_label, day)

            return render(request, "home.html", context)
    else:
        context = _get_home_context(None, request.user, year, week_label, day)

        return render(request, "home.html", context)


@login_required
@require_http_methods(["GET"])
def delete_progress(request, year, week_label, day, progress_id):
    _delete_progress(progress_id)

    redirect_uri = "/year/%s/week/%s/day/%s" % (year, week_label, day)

    return redirect(redirect_uri)


@login_required
@require_http_methods(["GET"])
def projects(request):
    context = _get_projects_context()

    t = loader.get_template('projects.html')
    
    return HttpResponse(t.render(Context(context)), content_type="text/javascript")


@login_required
def edit_progress(request, year, week_label, day, progress_id):
    if request.method == 'POST':
        form = ProgressEditForm(request.POST)

        if form.is_valid():
            return _save_progress(request.user, request.path, form, progress_id)
        else:
            context = _get_edit_progress_context(form, year, week_label, day, progress_id)
            return render(request, "edit-progress.html", context)
    else:
        context = _get_edit_progress_context(None, year, week_label, day, progress_id)
        return render(request, "edit-progress.html", context)