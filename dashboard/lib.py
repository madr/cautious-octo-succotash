import datetime

from core.models import Progress, Absence


def get_project_data(start_date, end_date, user=None):
    progresses = Progress.objects.filter(done_at__gte=start_date, done_at__lte=end_date)
    absences = Absence.objects.filter(done_at__gte=start_date, done_at__lte=end_date)

    if user:
        progresses = progresses.filter(user=user)
        absences = absences.filter(user=user)

    td = datetime.timedelta(days=1)

    ends_at = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    datasets = list()

    for progs in [progresses.filter(project__billable=True), progresses.filter(project__billable=False), absences]:
        d = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        labels = list()
        values = list()

        while d <= ends_at:
            values.append(sum([p.duration / 60.0 for p in progs.filter(done_at=d)]))
            labels.append(d.strftime('%a'))

            d += td

        datasets.append(dict(data=values))

    return datasets, labels

def get_week_data(start_date, end_date, user=None):
    progresses = Progress.objects.filter(done_at__gte=start_date, done_at__lte=end_date)

    if user:
        progresses = Progress.objects.filter(user=user)

    projects = sorted(set([p.project.name for p in progresses]))

    values = list()
    labels = list()

    for project in projects:
        values.append(sum([p.duration / 60.0 for p in progresses.filter(project__name=project)]))
        labels.append(project)

    return values, labels
