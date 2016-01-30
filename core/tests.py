from django.test import TestCase
from rest_framework.exceptions import ValidationError

from core.models import validate_duration


class ProgressesTestCase(TestCase):
    def test_it_does_not_allow_durations_that_is_not_quarters(self):

        with self.assertRaisesMessage(ValidationError, 'only even quarters allowed, for example: 15, 45, 180, 105'):
            validate_duration(13)
