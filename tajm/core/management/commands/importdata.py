import json

from django.core.management import BaseCommand
from django.core.management import CommandError

from tajm.core.models import Progress, Absence, TajmUser, Project, AbsenceCategory


def create_progress(progress):
    user, created = TajmUser.objects.get_or_create(first_name=progress['user_first_name'],
                                                   last_name=progress['user_last_name'],
                                                   email=progress['user_email'],
                                                   username=progress['user_name'])

    project, created = Project.objects.get_or_create(name=progress['project_name'],
                                                     billable=progress['project_billable'],
                                                     active=progress['project_active'])

    Progress.objects.create(duration=int(progress['duration']),
                    note=progress['note'],
                    done_at=progress['done_at'],
                    created_at=progress['created_at'],
                    user=user,
                    project=project)


def create_absence(absence):
    user, created = TajmUser.objects.get_or_create(first_name=absence['user_first_name'],
                                                   last_name=absence['user_last_name'],
                                                   email=absence['user_email'],
                                                   username=absence['user_name'])

    category, created = AbsenceCategory.objects.get_or_create(name=absence['category_name'],
                                                             active=absence['category_active'])

    Absence.objects.create(duration=int(absence['duration']),
                    note=absence['note'],
                    done_at=absence['done_at'],
                    created_at=absence['created_at'],
                    user=user,
                    category=category)


class Command(BaseCommand):
    help = 'import data for Tajm projects, absences, absence categories, progresses and users'

    def add_arguments(self, parser):
        parser.add_argument('source_file', nargs='+', type=str)

    def handle(self, *args, **options):
        if 'source_file' not in options:
            raise CommandError('Please provide a source file path')

        with open(options['source_file'][0], 'r') as f:
            data = json.loads(f.read())

        for progress in data[0]:
            create_progress(progress)
            pass
        for absence in data[1]:
            create_absence(absence)

        self.stdout.write(self.style.SUCCESS('Successfully imported tajm content'))
