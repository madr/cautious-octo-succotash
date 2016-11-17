import json

from django.core.management import BaseCommand
from django.core.management import CommandError

from core.models import Progress, Absence


def create_progress(progress):
    # get or create user

    # get or create project

    # create progress
    pass


def create_absence(absence):
    # get or create user

    # get or create absence category

    # create absence
    pass


class Command(BaseCommand):
    help = 'import data for Tajm projects, absences, absence categories, progresses and users'

    def add_arguments(self, parser):
        parser.add_argument('source_file', nargs='+', type=str)

    def handle(self, *args, **options):
        if 'source_file' not in options:
            raise CommandError('Please provide a source file path')

        with open(options['target_file'][0], 'w+') as f:
            data = json.loads(f.read())

        for progress in data[0]:
            create_progress(progress)
        for absence in data[1]:
            create_absence(absence)

        self.stdout.write(self.style.SUCCESS('Successfully imported tajm content'))
