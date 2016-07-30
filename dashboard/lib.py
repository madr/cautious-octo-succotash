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


def get_project_data(start_date, end_date, user=None):
    progresses = Progress.objects.filter(done_at__gte=start_date, done_at__lte=end_date)

    if user:
        progresses = progresses.filter(user=user)

    projects = sorted(set([p.project.name for p in progresses]))

    values = list()

    for project in projects:
        project_progresses = progresses.filter(project__name=project)
        values.append(dict(
            billable=project_progresses.first().project.billable,
            name=project,
            sum=(sum([p.duration for p in project_progresses])),
            count=len(project_progresses)
        ))

    return values


def get_absence_data(start_date, end_date, user=None):
    absences = Absence.objects.filter(done_at__gte=start_date, done_at__lte=end_date)

    if user:
        absences = absences.filter(user=user)

    absence_categories = sorted(set([p.category.name for p in absences]))

    values = list()

    for absence in absence_categories:
        absences_by_this_category = absences.filter(category__name=absence)
        values.append(dict(
            name=absence,
            sum=(sum([p.duration for p in absences_by_this_category])),
            count=len(absences_by_this_category)
        ))

    return values
