from django import forms
from haystack.forms import FacetedSearchForm, SearchForm


# todo: wait until Elastic Search 2 is supported by haystack
# class ProgressSearchForm(FacetedSearchForm):
class ProgressSearchForm(SearchForm):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def search(self):
        sqs = super(ProgressSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['start_date']:
            sqs = sqs.filter(done_at__gte=self.cleaned_data['start_date'])

        if self.cleaned_data['end_date']:
            sqs = sqs.filter(done_at__lte=self.cleaned_data['end_date'])

        return sqs
