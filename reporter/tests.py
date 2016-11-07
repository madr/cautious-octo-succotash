from core.models import Progress, Project
from django.contrib.sessions.backends.base import SessionBase
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.test import TestCase
from reporter.lib import ProgressAbsenceEditForm
from reporter.lib import _year_week_day, ProgressAbsenceForm
from datetime import datetime, timedelta
from reporter.views import report, edit_progress, delete_progress, projects
from django.contrib.auth.models import User


def _create_post_request_mock():
    request = HttpRequest()
    request.method = 'POST'
    request.path = '/year/2013/week/1/day/6'
    request.user = User.objects.create_user('John Doe')

    request.META['HTTP_HOST'] = '127.0.0.1'
    request.session = SessionBase()

    request.POST['duration'] = '00:15'
    request.POST['project'] = 'Test'
    request.POST['note'] = 'a note'
    request.POST['done_at'] = '2014-01-01'
    request.POST['done_at_year'] = '2014'
    request.POST['done_at_week'] = '4'
    request.POST['done_at_day'] = '5'

    return request


def _create_progress_mock(request, note='bla bla'):
    project = Project.objects.create(name='bla')
    project.save()

    progress = Progress.objects.create(
        done_at = '2014-01-01',
        duration = 30,
        user = request.user,
        note = note,
        project = project)
    progress.save()

    return progress


class YearWeekDayTestCase(TestCase):
    def test_year_week_day_internal(self):
        today = datetime.now().isocalendar()
        not_this_week = (datetime.now() + timedelta(days=21)).isocalendar()
        
        # sundays should be zero
        y, w, d, ii = _year_week_day(2011, 30, 7)
        self.assertEqual(d, 0)

        if today[2] == 7: day = 0
        else: day = today[2]

        # defaults to today
        y, w, d, ii = _year_week_day(today[0], today[1], today[2])
        self.assertEqual(y, today[0])
        self.assertEqual(w, today[1])
        self.assertEqual(d, day)
        self.assertEqual(ii, 2)

        # defaults to today
        y, w, d, ii = _year_week_day(None, None, None)
        self.assertEqual(y, today[0])
        self.assertEqual(w, today[1])
        self.assertEqual(d, day)
        self.assertEqual(ii, 2)

        # ii (is_index) can have 3 values:
        #
        # 0 - the date is niether in current week or current day
        # 1 - current week but not current day
        # 2 - current day and current week
 
        y, w, d, ii = _year_week_day(not_this_week[0], not_this_week[1], not_this_week[2])
        self.assertEqual(ii, 0)

        if today[2] > 1: another_day_in_current_week = today[2] - 1
        else: another_day_in_current_week = today[2] + 1

        y, w, d, ii = _year_week_day(today[0], today[1], another_day_in_current_week)
        self.assertEqual(ii, 1)
        
        y, w, d, ii = _year_week_day(today[0], today[1], today[2])
        self.assertEqual(ii, 2)


class ReporterFormsTestCase(TestCase):
    def test_form_when_ProgressForm_fields_are_incorrect(self):
        request = _create_post_request_mock()

        form = ProgressAbsenceForm(request.POST)
        self.assertEqual(form.is_valid(), True)

        request.POST['done_at'] = ''

        form = ProgressAbsenceForm(request.POST)
        self.assertEqual(form.is_valid(), False)

        request.POST['done_at'] = '2014-01-01'
        request.POST['note'] = ''

        form = ProgressAbsenceForm(request.POST)
        self.assertEqual(form.is_valid(), False)

        request.POST['note'] = 'asdasdasd'
        request.POST['project'] = ''

        form = ProgressAbsenceForm(request.POST)
        self.assertEqual(form.is_valid(), False)

        request.POST['project'] = 'asdasdasd'
        request.POST['duration'] = ''

        form = ProgressAbsenceForm(request.POST)
        self.assertEqual(form.is_valid(), False)


    def test_form_when_ProgressEditForm_fields_are_incorrect(self):
        request = _create_post_request_mock()

        form = ProgressAbsenceEditForm(request.POST)
        self.assertEqual(form.is_valid(), True)

        request.POST['done_at_week'] = ''

        form = ProgressAbsenceEditForm(request.POST)
        self.assertEqual(form.is_valid(), False)

        request.POST['done_at_week'] = '5'
        request.POST['done_at_day'] = ''

        form = ProgressAbsenceEditForm(request.POST)
        self.assertEqual(form.is_valid(), False)

        request.POST['done_at_day'] = '4'
        request.POST['done_at_year'] = ''

        form = ProgressAbsenceEditForm(request.POST)
        self.assertEqual(form.is_valid(), False)


class DeleteViewTestCase(TestCase):
    def test_delete_progress_and_redirect_back(self):
        request = _create_post_request_mock()
        request.method = 'GET'
        progress = _create_progress_mock(request, 'jagarheltunik')

        self.assertEqual(Progress.objects.filter(note='jagarheltunik').count(), 1)

        response = delete_progress(request, 2013, 1, 6, progress.id)

        self.assertEqual(Progress.objects.filter(note='jagarheltunik').count(), 0)
        self.assertEqual(response.status_code, 302)


class ReportViewTestCase(TestCase):
    def test_report_shows_page_on_get(self):
        request = _create_post_request_mock()

        request.method = 'GET'

        response = report(request, 2014, 1, 1)
        self.assertEqual(isinstance(response, HttpResponse), True)
        self.assertEqual(response.status_code, 200)


    def test_report_submit_returns_redirect_when_valid(self):
        request = _create_post_request_mock()

        response = report(request)
        self.assertEqual(isinstance(response, HttpResponseRedirect), True)
        self.assertEqual(response.status_code, 302)


    def test_report_submit_returns_page_with_form_errors_when_invalid(self):
        request = _create_post_request_mock()
        request.POST['note'] = ''

        response = report(request)
        self.assertEqual(isinstance(response, HttpResponse), True)
        self.assertEqual(response.status_code, 200)


class SaveProgressTestCase(TestCase):
    def test_it_saves_progress_to_database(self):
        request = _create_post_request_mock()
        request.POST['note'] = 'helvetesjavlar'

        self.assertEqual(Progress.objects.filter(note='helvetesjavlar').count(), 0)

        report(request)

        self.assertEqual(Progress.objects.filter(note='helvetesjavlar').count(), 1)


    def test_it_creates_project_if_not_existing(self):
        request = _create_post_request_mock()
        request.POST['project'] = 'helvetesjavlar'

        report(request)

        self.assertEqual(Project.objects.filter(name='helvetesjavlar').count(), 1)

        project = Project.objects.get(name='helvetesjavlar')

        self.assertEqual(project.billable, True)
        self.assertEqual(project.active, True)


class ProjectsViewTestCase(TestCase):
    def test_projects_returns_javascript(self):
        r = _create_post_request_mock()
        r.method = 'GET'

        response = projects(r)

        self.assertEqual(response.__getitem__('Content-Type'), 'text/javascript')


class EditProgressViewTestCase(TestCase):
    def test_report_shows_page_on_get(self):
        request = _create_post_request_mock()
        progress = _create_progress_mock(request)

        request.method = 'GET'

        response = edit_progress(request, 2014, 1, 1, progress.id)
        self.assertEqual(isinstance(response, HttpResponse), True)
        self.assertEqual(response.status_code, 200)


    def test_editprogress_submit_returns_redirect_when_valid(self):
        request = _create_post_request_mock()
        progress = _create_progress_mock(request)

        response = edit_progress(request, 2014, 4, 5, progress.id)
        self.assertEqual(isinstance(response, HttpResponseRedirect), True)
        self.assertEqual(response.status_code, 302)


    def test_editprogress_submit_returns_page_with_form_errors_when_invalid(self):
        request = _create_post_request_mock()
        progress = _create_progress_mock(request)
        request.POST['note'] = ''

        response = edit_progress(request, 2014, 4, 5, progress.id)

        self.assertEqual(isinstance(response, HttpResponse), True)
        self.assertEqual(response.status_code, 200)


    def test_editprogress_redirects_to_the_form_date_on_success(self):
        request = _create_post_request_mock()
        progress = _create_progress_mock(request)

        response = edit_progress(request, 2014, 4, 5, progress.id)

        self.assertEquals(response.status_code, 302)