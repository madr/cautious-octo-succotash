import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from core.lib import TimeUtil

from core.models import Progress, Absence, TajmUser, Project
from dashboard.lib import get_project_data, get_week_data, get_absence_data


@login_required
def list_users(request):
    return render(request, 'list_users.html', {
        'users': TajmUser.objects.filter(is_active=True, is_superuser=False).order_by('username')
    })


@login_required
def list_projects(request):
    return render(request, 'list_projects.html', {
        'projects': Project.objects.filter(active=True)
    })


@login_required
def project(request, id):
    return redirect('today')


@login_required
def dashboard(request):
    return redirect('today')


@login_required
def profile(request, user_id=None):
    if user_id:
        profile = TajmUser.objects.get(id=user_id)
    else:
        profile = TajmUser.objects.get(pk=request.user.id)

    all_progresses = profile.progress_set.all()

    total_time = sum([p.duration for p in all_progresses])
    total_projects = len(set([p.project.name for p in all_progresses]))

    try:
        billable_rank = int((sum([p.duration for p in all_progresses.filter(project__billable=True)]) / total_time) * 100)
    except ZeroDivisionError:
        billable_rank = None

    projects = sorted(get_project_data(all_progresses), key=lambda p: p['sum'], reverse=True)

    try:
        max_sum = max([p['sum'] for p in projects])
    except ValueError:
        max_sum = 0

    try:
        max_count = max([p['count'] for p in projects])
    except ValueError:
        max_count = 0

    most_recent_progresses = all_progresses[0:10]

    context = dict(
        profile=profile,
        total_time=total_time,
        total_projects=total_projects,
        projects=projects[0:10],
        max_sum=max_sum,
        max_count=max_count,
        most_recent_progresses=most_recent_progresses,
        billable_rank=billable_rank,
    )

    return render(request, 'profile.html', context=context)


@login_required
def time_comparison_bar_chart_data(request):
    if request.GET['from']:
        start_date = request.GET['from']
    else:
        start_date = datetime.date.today()

    if request.GET['from']:
        end_date = request.GET['to']
    else:
        end_date = datetime.date.today()

    datasets, labels = get_project_data(start_date, end_date, request.user)

    data = dict(datasets=datasets, labels=labels)

    return JsonResponse(data, safe=False)


@login_required
def projects_bar_chart_data(request):
    if request.GET['from']:
        start_date = request.GET['from']
    else:
        start_date = datetime.date.today()

    if request.GET['from']:
        end_date = request.GET['to']
    else:
        end_date = datetime.date.today()

    values, labels = get_week_data(start_date, end_date, request.user)

    data = dict(datasets=[dict(data=values)], labels=labels)

    return JsonResponse(data, safe=False)


@login_required
def week_summary(request, year, week_label):
    user = request.user

    year = int(year)
    week_label = int(week_label)

    week_start, week_end = TimeUtil.week_start_end(year, week_label)

    absences = user.absence_set.objects.filter(done_at__gte=week_start, done_at__lte=week_end)
    progresses = user.progress_set.filter(done_at__gte=week_start, done_at__lte=week_end)

    ww_absence_count = sum(absences.values('duration'))
    ww_project_count = len(set([p.project.name for p in progresses]))
    ww_progresses_count = progresses.count()
    ww_minute_count = sum([p.duration for p in progresses])
    ww_billable = sum([p.duration for p in progresses.filter(project__billable=True)])

    ww_project_toplist = get_project_data(progresses)
    ww_absence_toplist = get_absence_data(absences)
    ww_summary = get_week_data(week_start, week_end, user)

    try:
        ww_max_project_toplist_sum = max([v['sum'] for v in ww_project_toplist])
    except ValueError:
        ww_max_project_toplist_sum = None

    try:
        ww_max_project_toplist_count = max([v['count'] for v in ww_project_toplist])
    except ValueError:
        ww_max_project_toplist_count = None

    try:
        ww_max_absence_toplist_sum = max([v['sum'] for v in ww_absence_toplist])
    except ValueError:
        ww_max_absence_toplist_sum = None

    try:
        ww_max_absence_toplist_count = max([v['count'] for v in ww_absence_toplist])
    except ValueError:
        ww_max_absence_toplist_count = None

    try:
        ww_max_summary_progresses = max([v['progresses'] for v in ww_summary])
    except ValueError:
        ww_max_summary_progresses = None

    try:
        ww_max_summary_projects = max([v['projects'] for v in ww_summary])
    except ValueError:
        ww_max_summary_projects = None

    try:
        ww_max_summary_sum = max([v['sum'] for v in ww_summary])
    except ValueError:
        ww_max_summary_sum = None

    try:
        ww_billable_pc = int((ww_billable  / float(ww_minute_count)) * 100)
    except ZeroDivisionError:
        ww_billable_pc = 0

    context = {
        'week': week_label,
        'year': year,
        'week_start': week_start,
        'week_end': week_end,
        'prev_week': TimeUtil.prevweek(year, week_label),
        'next_week': TimeUtil.nextweek(year, week_label),
        'spoken_week': TimeUtil.period(year, week_label),

        'progresses': progresses,
        'absences': absences,

        'ww_absence_count': ww_absence_count,
        'ww_project_count': ww_project_count,
        'ww_progresses_count': ww_progresses_count,
        'ww_minute_count': ww_minute_count,
        'ww_billable': ww_billable_pc,
        'ww_nonbillable_count': ww_minute_count - ww_billable,
        'ww_project_toplist': ww_project_toplist,

        'ww_absence_toplist': ww_absence_toplist,

        'ww_max_absence_toplist_sum': ww_max_absence_toplist_sum,
        'ww_max_absence_toplist_count': ww_max_absence_toplist_count,
        'ww_max_project_toplist_sum': ww_max_project_toplist_sum,
        'ww_max_project_toplist_count': ww_max_project_toplist_count,
        'ww_max_summary_progresses': ww_max_summary_progresses,
        'ww_max_summary_sum': ww_max_summary_sum,
        'ww_max_summary_projects': ww_max_summary_projects,

        'ww_summary': ww_summary,
    }

    return render(request, 'week_summary.html', context)
