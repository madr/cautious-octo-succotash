from datetime import datetime

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from core.lib import TimeUtil
from core.models import Progress, Project, Absence, AbsenceCategory
from dashboard.lib import get_project_data, get_week_data


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['category', 'duration', 'done_at', 'user']


class ProgressAbsenceForm(forms.Form):
    '''manages progress submit from regular users.
    Uses an unbound form since a lot of logic is required for
    the form to work properly.'''
    duration = forms.TimeField(required=True)
    project_or_absence_category = forms.CharField(required=True)
    note = forms.CharField()
    done_at = forms.DateField()


class ProgressAbsenceEditForm(ProgressAbsenceForm):
    done_at_year = forms.IntegerField(required=True)
    done_at_week = forms.IntegerField(required=True)
    done_at_day = forms.IntegerField(required=True)


def _delete_progress(progress_id):
    progress = Progress.objects.get(pk=progress_id)

    year, week_label, day = TimeUtil.ywd(progress.done_at).split('-')

    progress.delete()

    return redirect('anyday', year=year, week_label=week_label, day=day)


def _save_progress(user, form, existing_id=None):
    # if the project does not yet exist in the db, a new project is created
    # with default values.
    project_name = form.cleaned_data['project_or_absence_category']

    try:
        existing_project = Project.objects.get(name=project_name)
    except ObjectDoesNotExist:
        existing_project = Project.objects.create(name=project_name)
        existing_project.save()

    duration = TimeUtil.to_minutes(form.cleaned_data['duration'].strftime('%H:%M'))
    note = form.cleaned_data['note']

    if existing_id is None:
        done_at = form.cleaned_data['done_at']
        progress = Progress.objects.create(project=existing_project,
                                           duration=duration,
                                           done_at=done_at,
                                           user=user,
                                           note=note)

        year, week_label, day = TimeUtil.ywd(done_at).split('-')

    else:
        progress = Progress.objects.get(pk=existing_id)

        year = form.cleaned_data['done_at_year']
        week_label = form.cleaned_data['done_at_week']
        day = form.cleaned_data['done_at_day']

        progress.project = existing_project
        progress.duration = duration
        progress.done_at = TimeUtil.ywd_to_date(year, week_label, day)
        progress.note = note

    progress.save()
    return redirect('anyday', year=year, week_label=week_label, day=day)


def _save_absence(user, form, existing_id=None):
    absence_category_name = form.cleaned_data['project_or_absence_category']

    try:
        existing_ac = AbsenceCategory.objects.get(name=absence_category_name)
    except ObjectDoesNotExist:
        return None

    duration = TimeUtil.to_minutes(form.cleaned_data['duration'].strftime('%H:%M'))
    note = form.cleaned_data['note']

    if existing_id is None:
        done_at = form.cleaned_data['done_at']
        absence = Absence.objects.create(category=existing_ac,
                                           duration=duration,
                                           done_at=done_at,
                                           user=user,
                                           note=note)

        year, week_label, day = TimeUtil.ywd(done_at).split('-')
    else:
        absence = Progress.objects.get(pk=existing_id)

        year = form.cleaned_data['done_at_year']
        week_label = form.cleaned_data['done_at_week']
        day = form.cleaned_data['done_at_day']

        absence.project = existing_ac
        absence.duration = duration
        absence.done_at = TimeUtil.ywd_to_date(year, week_label, day)
        absence.note = note

    absence.save()
    return redirect('anyday', year=year, week_label=week_label, day=day)


def _year_week_day(year, week_label, day):
    ''' 
    helper which which verifies input data 
    
    is_index check the date and return these values:

    0 - neither current week or current day
    1 - current week but not current day
    2 - current day
    '''
    today = datetime.now().isocalendar()

    if year is None and week_label is None and day is None:
        is_index = 2
    else:
        if int(year) == today[0] and int(week_label) == today[1]:
            if int(day) == today[2]:
                is_index = 2
            else:
                is_index = 1
        else:
            is_index = 0


    if year is None:
        year = int(today[0])

    if week_label is None:
        week_label = int(today[1])

    if day is None:
        day = int(today[2])

    # do not mess with sundays.
    if day is 7: day = 0

    return int(year), int(week_label), int(day), is_index


def _get_edit_progress_context(form, progress_id):
    progress = Progress.objects.get(pk=progress_id)

    year, week_label, day = TimeUtil.ywd(progress.done_at).split('-')

    if form is None:
        form = ProgressAbsenceEditForm(initial={
            'done_at_year': year,
            'done_at_week': week_label,
            'done_at_day': day,
            'done_at': progress.done_at,
            'note': progress.note,
            'duration': TimeUtil.hhmm(progress.duration),
            'project_or_absence_category': progress.project.name
        })

    context = {
        'progress_form': form
    }

    return context


def _get_reporter_context(progress_form, user, year, week_label, day):
    ''' The most seen page of the reporter app which shows a given day
     of a given week, with current week and current weekday as default.

    lets a logged in user view his progresses of the day and
    also submit another progress.

    From here, the user navigates within the same week (Mon-Sun),
    to next week and to previous week.

    A little note about week numbers
    --------------------------------

    `week_label` is the spoken week number, in the form 1-53,
    since that is what PEOPLE label it.

    In Python, however, it might be a bit confusing. Permalinks make
    uses of the 'week labels' instead of the actual week number.

     * The first week of a year according to datetime.strftime('%W') is week 0.
     * datetime.isocalendar() will return the spoken week number.

    So Beware! The app uses the 'week_label' wherever possible, and
    this decision make week number transformation to dates
    (ex 2013-01-01) a bit tricky since '%W' will result
    in 7 days mismatch.

    Yet, in particular years (ex 2012) when Jan 1 is on a Monday,
    datetime.strftime('%W') and datetime.isocalendar() will show the same
    week number. Thanks ...

    It is HIGHLY recommended to always use TimeUtil.ywd_to_date() when
    trying to create dates. '''

    year, week_label, day, is_index = _year_week_day(year,
                                                     week_label,
                                                     day)

    the_date = TimeUtil.ywd_to_date(year, week_label, day)
    progresses = user.progress_set.filter(done_at=the_date)
    absences = user.absence_set.filter(done_at=the_date)

    if progress_form is None:
        progress_form = ProgressAbsenceForm(initial={'done_at': the_date})

    week_start, week_end = TimeUtil.week_start_end(year, week_label)

    absence_count = sum([a.duration for a in absences])
    minute_count = sum([p.duration for p in progresses])
    project_count = len(set([p.project.name for p in progresses]))

    whole_week_progresses = user.progress_set.filter(done_at__gte=week_start, done_at__lte=week_end)

    ww_minute_count = sum([p.duration for p in whole_week_progresses])

    context = {
        'weekdays': TimeUtil.num_name_date(year, week_label),
        'week': week_label,
        'day': day,
        'year': year,
        'week_start': week_start,
        'week_end': week_end,
        'progress_form': progress_form,
        'absences': absences,
        'progresses': progresses,
        'minute_count': minute_count,
        'project_count': project_count,
        'absence_count': absence_count,
        'is_index': is_index > 0,
        'is_today': is_index == 2,
        'prev_week': TimeUtil.prevweek(year, week_label),
        'next_week': TimeUtil.nextweek(year, week_label),
        'spoken_week': TimeUtil.period(year, week_label),
        'ww_minute_count': ww_minute_count,
    }

    return context


def _delete_absence(absence_id):
    absence = Absence.objects.get(pk=absence_id)
    done_at = absence.done_at
    absence.delete()

    return TimeUtil.ywd(done_at).split('-')