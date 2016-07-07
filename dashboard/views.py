from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from haystack.views import FacetedSearchView, SearchView


@login_required
def dashboard(request):
    return redirect('home')


# todo: wait until Elastic Search 2 is supported by haystack
# class ProgressSearchView(FacetedSearchView):
class ProgressSearchView(SearchView):
    def get_queryset(self):
        queryset = super(ProgressSearchView, self).get_queryset()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ProgressSearchView, self).get_context_data(*args, **kwargs)
        return context
