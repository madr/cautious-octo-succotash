from datetime import datetime

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from legacy.utils import SumUtil, records_to_dict
from core.lib import TimeUtil
from core.models import Progress, Project, Absence


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['category', 'duration', 'done_at', 'user']


class ProgressForm(forms.Form):
    '''manages progress submit from regular users.
    Uses an unbound form since a lot of logic is required for
    the form to work properly.'''
    duration = forms.TimeField(required=True)
    project = forms.CharField(required=True)
    note = forms.CharField()
    done_at = forms.DateField()


class ProgressEditForm(ProgressForm):
    done_at_year = forms.IntegerField(required=True)
    done_at_week = forms.IntegerField(required=True)
    done_at_day = forms.IntegerField(required=True)


def _delete_progress(progress_id):
    progress = Progress.objects.get(pk=progress_id)
    progress.delete()


def _get_projects_context():
    context = {
        'projects': Project.objects.filter(active=True)
    }

    return context


def _save_progress(user, form, existing_id=None):
    '''typical POST action for the _show_day method. It stores the
    submitted progress to db.

    if the project does not yet exist in the db, a new project is created
    with default values.'''
    project_name = form.cleaned_data['project']

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


def _get_edit_progress_context(form, year, week_label, day, progress_id):
    progress = Progress.objects.get(pk=progress_id)

    if form is None:
        form = ProgressEditForm(initial={
            'done_at_year': year,
            'done_at_week': week_label,
            'done_at_day': day,
            'done_at': progress.done_at,
            'note': progress.note,
            'duration': TimeUtil.hhmm(progress.duration),
            'project': progress.project.name
        })

    context = {
        'progress_form': form
    }

    return context


def _get_home_context(progress_form, user, year, week_label, day):
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

    weekdays = TimeUtil.num_name_date(year, week_label)

    the_date = TimeUtil.ywd_to_date(year, week_label, day)
    progresses = Progress.objects.filter(user=user, done_at=the_date)
    progresses_as_list = records_to_dict(progresses)
    absences = Absence.objects.filter(user=user, done_at=the_date)

    if progress_form is None:
        progress_form = ProgressForm(initial={'done_at': the_date})

    absence_form = AbsenceForm(initial={'user': user})

    context = {
        'weekdays': weekdays,
        'week': week_label,
        'day': day,
        'year': year,
        'date': TimeUtil.ywd_to_date(year, week_label, day),
        'progress_form': progress_form,
        'absence_form': absence_form,
        'absences': absences,
        'progresses': progresses,
        'minute_count': TimeUtil.duration(SumUtil.minutes(progresses_as_list)),
        'project_count': SumUtil.projects(progresses_as_list),
        
        'is_index': is_index > 0,
        'is_today': is_index == 2,
        'prev_week': TimeUtil.prevweek(year, week_label),
        'next_week': TimeUtil.nextweek(year, week_label),
        'spoken_week': TimeUtil.period(year, week_label)
    }

    return context


def _delete_absence(absence_id):
    absence = Absence.objects.get(pk=absence_id)
    done_at = absence.done_at
    absence.delete()

    return TimeUtil.ywd(done_at).split('-')