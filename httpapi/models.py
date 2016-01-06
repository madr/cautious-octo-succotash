from django.db import models
from oauth2_provider.models import AbstractApplication

from core.models import Customer


class SemirhageApplication(AbstractApplication):
    customer = models.ForeignKey(Customer)
