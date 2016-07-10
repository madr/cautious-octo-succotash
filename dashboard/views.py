import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from haystack.views import FacetedSearchView, SearchView

from core.models import Progress, Absence


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

    progresses = Progress.objects.filter(user=request.user, done_at__gte=start_date, done_at__lte=end_date)
    absences = Absence.objects.filter(user=request.user, done_at__gte=start_date, done_at__lte=end_date)

    td = datetime.timedelta(days=1)

    ends_at = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    datasets = list()

    for progs in [progresses.filter(project__billable=True), progresses.filter(project__billable=False), absences]:
        d = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        labels = list()
        values = list()

        while d <= ends_at:
            values.append(sum([p.duration / 60.0 for p in progs.filter(done_at=d)]))
            labels.append(d.strftime('%a'))

            d += td

        datasets.append(dict(data=values))

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

    progresses = Progress.objects.filter(user=request.user, done_at__gte=start_date, done_at__lte=end_date)
    projects = sorted(set([p.project.name for p in progresses]))

    values = list()
    labels = list()

    for project in projects:
        values.append(sum([p.duration / 60.0 for p in progresses.filter(project__name=project)]))
        labels.append(project)

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