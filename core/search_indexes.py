import datetime
from haystack import indexes
from core.models import Progress


class ProgressIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    duration = indexes.IntegerField(model_attr='duration')
    project = indexes.CharField(model_attr='project', faceted=True)
    user = indexes.CharField(model_attr='user', faceted=True)
    done_at = indexes.DateTimeField(model_attr='done_at')
    created_at = indexes.DateTimeField(model_attr='created_at')

    def get_model(self):
        return Progress

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(done_at__lte=datetime.datetime.now())