import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from haystack.views import FacetedSearchView, SearchView
from core.lib import TimeUtil

from core.models import Progress, Absence
from dashboard.lib import get_project_data, get_week_data


@login_required
def dashboard(request):
    return redirect('today')


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


# todo: wait until Elastic Search 2 is supported by haystack
# class ProgressSearchView(FacetedSearchView):
class ProgressSearchView(SearchView):
    def get_queryset(self):
        queryset = super(ProgressSearchView, self).get_queryset()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ProgressSearchView, self).get_context_data(*args, **kwargs)
        return context


@login_required
def week_summary(request, year, week_label):
    user = request.user

    year = int(year)
    week_label = int(week_label)

    week_start, week_end = TimeUtil.week_start_end(year, week_label)

    whole_week_absences = Absence.objects.filter(user=user, done_at__gte=week_start, done_at__lte=week_end)
    whole_week_progresses = Progress.objects.filter(user=user, done_at__gte=week_start, done_at__lte=week_end)

    ww_absence_count = sum([a.duration for a in whole_week_absences])
    ww_project_count = len(set([p.project.name for p in whole_week_progresses]))
    ww_progresses_count = whole_week_progresses.count()
    ww_minute_count = sum([p.duration for p in whole_week_progresses])
    ww_billable = sum([p.duration for p in whole_week_progresses.filter(project__billable=True)])

    ww_project_toplist = get_project_data(week_start, week_end, user)
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

        'ww_absence_count': ww_absence_count,
        'ww_project_count': ww_project_count,
        'ww_progresses_count': ww_progresses_count,
        'ww_minute_count': ww_minute_count,
        'ww_billable': ww_billable_pc,
        'ww_nonbillable_count': ww_minute_count - ww_billable,
        'ww_project_toplist': ww_project_toplist,

        'ww_max_project_toplist_sum': ww_max_project_toplist_sum,
        'ww_max_project_toplist_count': ww_max_project_toplist_count,
        'ww_max_summary_progresses': ww_max_summary_progresses,
        'ww_max_summary_sum': ww_max_summary_sum,
        'ww_max_summary_projects': ww_max_summary_projects,

        'ww_summary': ww_summary,
    }

    return render(request, 'week_summary.html', context)
