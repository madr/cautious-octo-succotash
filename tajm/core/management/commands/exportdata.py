import json

from django.core.management import BaseCommand
from django.core.management import CommandError

from tajm.core.models import Progress, Absence


class Command(BaseCommand):
    help = 'exports essential data for Tajm projects, absences, absence categories, progresses and users'

    def add_arguments(self, parser):
        parser.add_argument('target_file', nargs='+', type=str)

    def handle(self, *args, **options):
        if 'target_file' not in options:
            raise CommandError('Please provide a target file path')

        progresses = list()
        absentia = list()

        for progress in Progress.objects.all():
            progresses.append({
                'duration': progress.duration,
                'note': progress.note,
                'done_at': progress.done_at.strftime('%Y-%m-%d'),
                'created_at': progress.created_at.strftime('%Y-%m-%d'),
                'project_name': progress.project.name,
                'project_billable': progress.project.billable,
                'project_active': progress.project.active,
                'user_name': progress.user.username,
                'user_email': progress.user.email,
                'user_first_name': progress.user.first_name,
                'user_last_name': progress.user.last_name,
            })
        for absence in Absence.objects.all():
            absentia.append({
                'duration': absence.duration,
                'note': absence.note,
                'done_at': absence.done_at.strftime('%Y-%m-%d'),
                'created_at': absence.created_at.strftime('%Y-%m-%d'),
                'category_name': absence.category.name,
                'category_active': absence.category.active,
                'user_name': absence.user.username,
                'user_email': absence.user.email,
                'user_first_name': absence.user.first_name,
                'user_last_name': absence.user.last_name,
            })

        with open(options['target_file'][0], 'w+') as f:
            f.write(json.dumps([progresses, absentia]))

        self.stdout.write(self.style.SUCCESS('Successfully exported tajm content'))