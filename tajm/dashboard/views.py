import datetime

from django.contrib.auth.decorators import login_required
from django.db.models.functions.datetime import ExtractWeekDay
from django.http import JsonResponse
from django.shortcuts import redirect, render

from tajm.core.lib import TimeUtil
from tajm.core.models import TajmUser, Project, Deadline, Absence, Progress
from tajm.dashboard.lib import get_project_data, get_week_data, get_absence_data, generate_activity_table, \
    get_weekday_summary, get_user_data


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
def list_deadlines(request):
    today = datetime.date.today()
    return render(request, 'list_deadlines.html', {
        'deadlines': Deadline.objects.filter(ends_at__isnull=False),
        'deadlines_without_date': Deadline.objects.filter(ends_at__isnull=True)
    })


@login_required
def project(request, id):
    return redirect('today')


@login_required
def deadline(request, id):
    return redirect('today')


@login_required
def dashboard(request):
    today = datetime.date.today()
    year, week, day = today.isocalendar()
    this_week = TimeUtil.period(year, week)
    week_start, week_end = TimeUtil.week_start_end(year, week)
    month_started, month_ended = TimeUtil.month_start_end(2015, 30)

    absences = Absence.objects.filter(done_at__gte=week_start, done_at__lte=week_end)
    progresses = Progress.objects.filter(done_at__gte=week_start, done_at__lte=week_end)

    absences = sum([a.duration for a in absences])
    projects = len(set([p.project.name for p in progresses]))
    minutes = sum([p.duration for p in progresses])
    billable = sum([p.duration for p in progresses.filter(project__billable=True)])

    people = sorted(get_user_data(done_at__lte=month_ended, done_at__gte=month_started), key=lambda x: x['progresses'],
                    reverse=True)

    try:
        db = (minutes - billable) / minutes
    except ZeroDivisionError:
        db = 100

    return render(request, 'dashboard.html', {
        'absences': absences,
        'projects': projects,
        'minutes': minutes,
        'people': people,
        'db': db,
        'year': year,
        'week': week,
        'today': today,
        'this_week': this_week,
        'deadlines': Deadline.objects.filter(ends_at__gte=datetime.date.today())
    })


@login_required
def user_activity(request, user_id):
    profile = TajmUser.objects.get(pk=user_id)
    all_progresses = profile.progress_set.annotate(weekday=ExtractWeekDay('done_at')).all().reverse()
    y, w, d = all_progresses.first().done_at.isocalendar()

    activity = list()
    for y in range(y, datetime.date.today().year + 1):
        start_at = datetime.date(y, 1, 1)
        stop_at = start_at + datetime.timedelta(days=(26 * 7 - 1))

        activity.append([
            '%s - %s %s' % (start_at.strftime('%d %B'), stop_at.strftime('%d %B'), y),
            generate_activity_table(
                all_progresses.filter(done_at__gte=start_at, done_at__lte=stop_at),
                start_at,
                stop_at,
            )
        ])

        start_at = stop_at + datetime.timedelta(days=1)
        stop_at = datetime.date(y, 12, 31)

        activity.append([
            '%s - %s %s' % (start_at.strftime('%d %B'), stop_at.strftime('%d %B'), y),
            generate_activity_table(
                all_progresses.filter(done_at__gte=start_at, done_at__lte=stop_at),
                start_at,
                stop_at,
            )
        ])

    return render(request, 'user_activity.html', {
        'profile': profile,
        'progresses': all_progresses,
        'activity': activity
    })


@login_required
def profile(request, user_id=None):
    if user_id:
        profile = TajmUser.objects.get(id=user_id)
    else:
        profile = TajmUser.objects.get(pk=request.user.id)

    all_progresses = profile.progress_set.annotate(weekday=ExtractWeekDay('done_at')).all()

    total_time = sum([p.duration for p in all_progresses])
    total_projects = len(set([p.project.name for p in all_progresses]))

    try:
        billable_rank = int(
            (sum([p.duration for p in all_progresses.filter(project__billable=True)]) / total_time) * 100)
    except ZeroDivisionError:
        billable_rank = None

    projects = sorted(get_project_data(all_progresses, user=profile), key=lambda p: p['sum'], reverse=True)

    try:
        max_sum = max([p['sum'] for p in projects])
    except ValueError:
        max_sum = 0

    try:
        max_count = max([p['count'] for p in projects])
    except ValueError:
        max_count = 0

    most_recent_progresses = all_progresses[0:10]

    return render(request, 'profile.html', dict(
        profile=profile,
        total_time=total_time,
        total_projects=total_projects,
        projects=projects[0:10],
        max_sum=max_sum,
        max_count=max_count,
        most_recent_progresses=most_recent_progresses,
        billable_rank=billable_rank,
        wdd=get_weekday_summary(all_progresses.reverse())
    ))


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
    year = int(year)
    week_label = int(week_label)

    week_start, week_end = TimeUtil.week_start_end(year, week_label)

    absences = Absence.objects.filter(done_at__gte=week_start, done_at__lte=week_end)
    progresses = Progress.objects.filter(done_at__gte=week_start, done_at__lte=week_end)

    ww_absence_count = sum([a.duration for a in absences])
    ww_project_count = len(set([p.project.name for p in progresses]))
    ww_progresses_count = progresses.count()
    ww_minute_count = sum([p.duration for p in progresses])
    ww_billable = sum([p.duration for p in progresses.filter(project__billable=True)])

    ww_project_toplist = get_project_data(progresses.filter(project__billable=True), done_at__gte=week_start,
                                          done_at__lte=week_end)
    ww_project_nb_toplist = get_project_data(progresses.filter(project__billable=False), done_at__gte=week_start,
                                             done_at__lte=week_end)
    ww_absence_toplist = get_absence_data(absences, done_at__gte=week_start, done_at__lte=week_end)
    ww_summary = get_week_data(week_start, week_end)

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
        ww_billable_pc = int((ww_billable / float(ww_minute_count)) * 100)
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
        'ww_project_nb_toplist': ww_project_nb_toplist,

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


@login_required
def current_week_summary(request):
    year, week_label, day = datetime.date.today().isocalendar()
    return week_summary(request, year, week_label)
