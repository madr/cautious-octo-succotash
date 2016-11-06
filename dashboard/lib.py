import datetime

from core.models import Progress, Absence


def get_week_data(start_date, end_date, user=None):
    progresses = Progress.objects.filter(done_at__gte=start_date, done_at__lte=end_date)
    absences = Absence.objects.filter(done_at__gte=start_date, done_at__lte=end_date)

    if user:
        progresses = progresses.filter(user=user)
        absences = absences.filter(user=user)

    td = datetime.timedelta(days=1)

    d = start_date
    values = list()

    while d <= end_date:
        progs_day = progresses.filter(done_at=d)

        values.append(dict(
            day=d,
            sum=sum([p.duration for p in progs_day]),
            absences=sum([p.duration for p in absences.filter(done_at=d)]),
            progresses=progs_day.count(),
            projects=len(set([p.project.name for p in progs_day])),
        ))

        d += td

    return values


def get_project_data(progresses, **kwargs):
    projects = set([p.project for p in progresses])

    values = list()

    for project in projects:
        values.append(dict(
            billable=project.billable,
            name=project.name,
            sum=(sum([p.duration for p in project.progress_set.filter(**kwargs)])),
            count=project.progress_set.filter(**kwargs).count()
        ))

    return sorted(values, key=lambda x: x['sum'], reverse=True)


def get_absence_data(absences, **kwargs):
    absence_categories = set([p.category for p in absences])

    values = list()

    for category in absence_categories:
        values.append(dict(
            name=category.name,
            sum=(sum([p.duration for p in category.absence_set.filter(**kwargs)])),
            count=category.absence_set.filter(**kwargs).count()
        ))

    return sorted(values, key=lambda x: x['sum'], reverse=True)
