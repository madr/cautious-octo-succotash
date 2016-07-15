import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from haystack.views import FacetedSearchView, SearchView

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