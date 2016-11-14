import datetime

from core.lib import TimeUtil
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


def generate_activity_table(progress_set, start_date, end_date):
    one_week = datetime.timedelta(days=7)
    r = range(0, 7)
    y, w, d = start_date.isocalendar()
    first_mon = TimeUtil.ywd_to_date(y, w, 1)
    y, w, d = end_date.isocalendar()
    last_sun = TimeUtil.ywd_to_date(y, w, 7)
    l = int((last_sun - first_mon).days / 7) + 1

    day_dates = [first_mon + datetime.timedelta(days=d) for d in r]

    data = [[day_dates[d].strftime('%a'), [[]]] for d in r]

    for progress in progress_set:
        i = progress.weekday - 2 if progress.weekday > 1 else 6

        if day_dates[i] < progress.done_at:
            data[i][1].append([])

            d = day_dates[i] + one_week
            while d < progress.done_at:
                data[i][1].append([])
                d += one_week

        day_dates[i] = progress.done_at
        data[i][1][-1].append(progress)

    for j in r:
        while len(data[j][1]) < l:
            data[j][1].append([])

    m = first_mon
    week_numbers = list()
    while m < last_sun:
        week_numbers.append(m.isocalendar()[1])
        m += one_week

    return [data, week_numbers]