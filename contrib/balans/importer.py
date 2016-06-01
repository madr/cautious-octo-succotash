# -*- coding: utf-8 -*-
import django
django.setup()

from django.contrib.auth.models import User
from contrib.balans.lib.random import names

from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

from xlsx import Workbook
from core.models import Project, Progress

in_file = '/Users/ay/Dropbox/tajmme-shared/all-tid-201506-201509.xlsx'


def _save_progress(data):
    project_name = data['project']
    user_name = data['user']

    try:
        existing_project = Project.objects.get(name=project_name)
    except ObjectDoesNotExist:
        existing_project = Project.objects.create(name=project_name)
        existing_project.save()

    try:
        existing_user = User.objects.get(username=user_name)
    except ObjectDoesNotExist:
        existing_user = User.objects.create(username=user_name)
        existing_user.save()

    progress = Progress.objects.create(project=existing_project,
                                       duration=data['duration'],
                                       done_at=data['done_at'],
                                       user=existing_user,
                                       note=data['note'])

    progress.save()


def import_from_xlsx():
    book = Workbook(in_file)

    for sheet in book:
        for i, row in sheet.rowsIter():
            if i == 1:
                continue

            description = '(left blank)'

            if len(row) == 21:
                description = row[20].value

            done_at = datetime.strptime(str(row[5].value), '(%Y, %m, %d, 0, 0, 0)')

            project = row[1].value

            _save_progress(dict(done_at=done_at.strftime('%Y-%m-%d'), project=project, user=names[int(row[2].value)],
                           duration=int(float(row[15].value) * 60), note=description))


if __name__ == '__main__':
    import_from_xlsx()
