#coding: utf-8
import operator
from django.core.mail import send_mail
import os
import random
import string
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext
from datetime import datetime, timedelta
from time import strptime
import re

# From Monday to Thursday: 
#    the week belongs to the current year.
# From Friday: the week
#   the week belongs to the next year.
#
# why Friday is the magic day? 
#
# have a look. It is helluwah mess, 
# you have been warned: 
#   http://sv.wikipedia.org/wiki/Vecka#Veckonummer
the_magic_day = 5
trimmer_a = re.compile('([^\d])0(\d) ')
trimmer_b = re.compile('^0(\d) ')

days = [u"Sön", u"Mån", u"Tis",
        u"Ons", u"Tor", u"Fre",
        u'Lör', u"Sön"]


class Investigator:
    """
    UNTESTED

    Should be converted to django anyway
    """
    def __init__(self, flask_args):
        self.flask_args = flask_args


    def get_mongo_filters(self):
        '''
        Expected formats:

        skip = <int>
        limit = <int>
        from = "%Y-%m-%d"
        to = "%Y-%m-%d"
        users = "one;two;three;four the fools;edward the fifth"
        projects = "WIDE;STAMPENCOM;MOBILNEXT;I2I"
        '''

        q = {}
        limit = None
        skip = None
        args = self.flask_args

        # limit if any
        if args.get("limit") is not None:
            limit = args.get("limit")

        # offset if any
        if args.get("skip") is not None:
            skip = args.get("skip")

        # default: no end is set.
        datebefore = None
        if args.get("to") is not None and len(args.get("to").split("-")) is 3:
            y, m, d = args.get("to").split("-")
            try:
                datebefore = datetime(int(y), int(m), int(d), 23, 59, 59)
            except ValueError:
                pass

        # default: start is not set.
        dateafter = None
        if args.get("from") is not None and len(args.get("from").split("-")) is 3:
            y, m, d = args.get("from").split("-")
            try:
                dateafter = datetime(int(y), int(m), int(d), 0, 0, 0)
            except ValueError:
                pass

        if dateafter is not None:
            date_range = {"$gte": dateafter}
        
            if datebefore is not None:
                date_range["$lte"] = datebefore

            q["done_at"] = date_range

        # owners
        if args.get("users") is not None:
            users = args.getlist("users")
            q["owner_name"] = {"$in": users}

        # projects
        if args.get("projects") is not None:
            projects = args.getlist("projects")
            q["project"] = {"$in": projects}

        return q, limit, skip


class Masturbation:
    """
    Abstracted object which can evaluate pretty much everything 
    that is to be known about progresses reported. 
    """
    _average = None
    _billable = None
    _billable_percent = None
    _billable_per_user = None
    _longest = None
    _median = None
    _minutes_per_project = None
    _minutes_per_user = None
    _projects_count = None
    _projects_per_user = None
    _progresses = None
    _progresses_count = None
    _sorted_progresses = None
    _shortest = None
    _total_time = None
    _users_per_project = None
    _users_count = None


    def __init__(self, progresses):
        self._progresses = progresses


    def average(self):
        if self._average is None:
            progresses_count = len(self._progresses)
            total_time = SumUtil.minutes(self._progresses)

            average = total_time / float(progresses_count)

            self._average = TimeUtil.correct(average)

        return self._average


    def billable(self):
        if self._billable is None:
            self._billable = SumUtil.minutes_per_x(u"billable", self._progresses)
        return self._billable


    def billable_percent(self):
        if self._billable_percent is None:
            billables = self.billable()

            if "yes" in billables:
                 yes = float(billables["yes"])
            else:
                self._billable_percent = 0

            if "no" in billables:
                no = float(billables["no"])
            else:
                self._billable_percent = 100

            if self._billable_percent is None:
                self._billable_percent = int((yes / (yes + no)) * 100)
        return self._billable_percent


    def billable_per_user(self):
        if self._billable_per_user is None:
            self._billable_per_user = SumUtil.billable_per_x(u"owner_name", self._progresses)
        return self._billable_per_user


    def longest(self):
        if self._longest is None:
            if self._sorted_progresses is None:
                self._sorted_progresses = sorted(self._progresses, key=operator.itemgetter("minutes"))

        self._longest = self._sorted_progresses[-1]

        return self._longest


    def median(self):
        if len(self._progresses) == 0:
            return None

        if self._median is None:
            if len(self._progresses) <= 2:
                self._median = self._progresses[0]
            else:
                if self._sorted_progresses is None:
                    self._sorted_progresses = sorted(self._progresses, key=operator.itemgetter("minutes"))

                median_index = int( (len(self._sorted_progresses) + 1) / 2.0)

                self._median = self._sorted_progresses[median_index]

        return self._median


    def minutes_per_project(self):
        if self._minutes_per_project is None:
            self._minutes_per_project = SumUtil.minutes_per_x(u"project", self._progresses)
        return self._minutes_per_project


    def minutes_per_user(self):
        if self._minutes_per_user is None:
            self._minutes_per_user = SumUtil.minutes_per_x(u"owner_name", self._progresses)
        return self._minutes_per_user


    def progresses(self):
        return self._progresses


    def progresses_count(self):
        if self._progresses_count is None:
            self._progresses_count = len(self._progresses)
        return self._progresses_count


    def projects_count(self):
        if self._projects_count is None:
            self._projects_count = SumUtil.projects(self._progresses)
        return self._projects_count


    def projects_per_user(self):
        if self._projects_per_user is None:
            self._projects_per_user = SumUtil.x_per_y(u"project", u"owner_name", self._progresses)
        return self._projects_per_user


    def shortest(self):
        if self._shortest is None:
            if self._sorted_progresses is None:
                self._sorted_progresses = sorted(self._progresses, key=operator.itemgetter("minutes"))

        if len(self._sorted_progresses) >= 3:
            self._shortest = self._sorted_progresses[0]

        return self._shortest


    def total_time(self):
        if self._total_time is None:
            self._total_time = SumUtil.minutes(self._progresses)
        return self._total_time


    def users_count(self):
        if self._users_count is None:
            self._users_count = SumUtil.count("owner", self._progresses)
        return self._users_count


    def users_per_project(self):
        if self._users_per_project is None:
            self._users_per_project = SumUtil.x_per_y(u"owner_name", u"project", self._progresses)
        return self._users_per_project


class SumUtil:
    ''' Class with a set of static methods to sum progresses. '''
    def __init__(self):
        pass


    @staticmethod
    def minutes_per_x(filter, progresses):
        '''
        group and sum progresses by project 
        '''
        minutes = {}

        for p in progresses:
            if p[filter] not in minutes:
                minutes[p[filter]] = 0
            minutes[p[filter]] = minutes[p[filter]] + p["minutes"]

        return minutes # sorted(minutes.items(), key=lambda x: x[1], reverse=True)


    @staticmethod
    def x_per_y(x, y, progresses):
        '''
        group and sum anything by anything 
        '''
        ys = {}

        for p in progresses:
            if p[y] not in ys:
                ys[p[y]] = []
            if p[x] not in ys[p[y]]:
                ys[p[y]].append(p[x])

        sorted_ys = {}
        for v, x in ys.iteritems():
            sorted_ys[v] = sorted(x)

        return sorted_ys


    @staticmethod
    def billable_per_x(x, progresses):
        xs = {}

        for p in progresses:
            if p[x] not in xs:
                xs[p[x]] = [0, 0]
            
            index = 1
            if p["billable"]: index = 0

            xs[p[x]][index] = xs[p[x]][index] + p["minutes"]

        xs2 = {}
        for v, x in xs.iteritems():
            if x[0] == 0:
                xs2[v] = 0
            else:    
                xs2[v] = int( float(x[0] / float(x[0] + x[1]) ) * 100)

        return xs2


    @staticmethod
    def minutes(progresses):
        ''' sum all minutes in one dictionary, also
        compatible with mongodb result set '''
        try:
            return sum([x["minutes"] for x in progresses])
        except:
            return sum([x[0] for x in progresses])


    @staticmethod
    def count(filter, progresses):
        ''' find unique projects in a dict, compatible with mongodb result set '''
        return len(set([x[filter] for x in progresses]))


    @staticmethod
    def projects(progresses):
        ''' find unique projects in a dict, compatible with mongodb result set '''
        return SumUtil.count("project", progresses)


class TimeUtil:
    # TODO: städa upp, kolla vilka som fortfarande används!
    ''' Class with a set of static methods to manage time and progresses. '''
    def __init__(self):
        pass


    @staticmethod
    def correct(anything):
        ''' make sure a duration (in minutes) is whole quarters. '''
        try:
            duration = int(anything)
        except ValueError:
            duration = 15

        if duration % 15 is not 0:
            duration += 15 - (duration % 15)

        return duration


    @staticmethod
    def to_minutes(hhmm):
        ''' calculates the number of minutes of a timestamp (hh:mm). '''
        hhmm = hhmm.split(":")

        minutes = int(hhmm[0]) * 60
        minutes = minutes + int(hhmm[1])

        return minutes


    @staticmethod
    def duration(minutes):
        ''' transform a duration (in minutes) to spoken time '''
        hh = (minutes - (minutes % 60)) / 60
        mm = minutes % 60
        hh_label = ugettext("timmar")

        if hh == 1:
            hh_label = ugettext("timme")

        if hh == 0:
            return "%d %s" % (mm, ugettext("minuter"))

        if mm == 0:
            return "%d %s" % (hh, hh_label)

        ret = "%d %s, %d %s" % (hh, hh_label, mm, ugettext("minuter"))

        return ret


    @staticmethod
    def hhmm(minutes):
        ''' transforms minutes to a timestamp string (HH:MM) '''
        hh = (minutes - (minutes % 60)) / 60
        mm = minutes % 60
        return "%02d:%02d" % (hh, mm)


    @staticmethod
    def ddmm(ymd):
        ''' transforms YYYY-MM-DD to DD/MM '''
        y, m, d = ymd.split("-")
        return "%d/%d" % (int(d), int(m))


    @staticmethod
    def weekday(date_obj):
        ''' return the name of a weekday (0-6) '''
        return days[int(date_obj.strftime("%w"))]


    @staticmethod
    def prettydate(date_obj):
        ''' return a date in the form <year>-<month>-<day> '''
        today = datetime.today()
        min1day = timedelta(days=1)
        min1week = timedelta(days=8)

        if date_obj > (today - min1day):
            return ugettext(u"idag")

        if date_obj > (today - min1day - min1day):
            return ugettext(u"igår")

        if date_obj > (today - min1week):
            return "i %ss" % TimeUtil.weekday(date_obj).lower()

        return date_obj.strftime("%Y-%m-%d")


    @staticmethod
    def ymd(date_obj):
        ''' return a date in the form <year>-<month>-<day> '''
        return date_obj.strftime("%Y-%m-%d")


    @staticmethod
    def ywd(date_obj):
        ''' return a date in the form <year>-<week>-<day>,
        where week is the SPOKEN week (1-53)'''
        return "%d-%d-%d" % date_obj.isocalendar()


    @staticmethod
    def week_start_end(year, week):
        week_started = TimeUtil.ywd_to_date(year, week, 1)
        week_ended = week_started + timedelta(days=6)
        
        return week_started, week_ended


    @staticmethod
    def num_name_date(year, week):
        weekdays = []

        for i in range(1,8):
            date = TimeUtil.ywd_to_date(year, week, i)
            weekdays.append((i, date))

        return weekdays


    @staticmethod
    def period(year, week):
        ''' return a date in the form <year>-<week>-<day> '''
        # get starting date and ending date of week
        week_started, week_ended = TimeUtil.week_start_end(year, week)

        reduced = "%d %b %Y"
        if week_started.year == week_ended.year:
            reduced = "%d %b"
            if week_started.month == week_ended.month:
                reduced = "%d"

        period = "%s - %s" % (week_started.strftime(reduced), 
                              week_ended.strftime("%d %b %Y"))

        period = trimmer_a.sub(r'\1\2 ', period)
        period = trimmer_b.sub(r'\1 ', period)
        
        return period


    @staticmethod
    def prevweek(year, week):
        return TimeUtil.another_week(year, week, -1)


    @staticmethod
    def nextweek(year, week):
        return TimeUtil.another_week(year, week, 1)


    @staticmethod
    def another_week(year, week, diff):
        future = (TimeUtil.ywd_to_date(year, week, the_magic_day) + timedelta(days=7 * diff))

        future_yw = future.isocalendar()

        return (future_yw[0], future_yw[1])


    @staticmethod
    def ywd_to_date(year, week_label, day):
        # Sundays mess with strptime, make sure it is 0.
        if day == 7: day = 0

        datestruct = strptime("%d %d %d" % (year, week_label, day), "%Y %W %w")
        date = datetime(datestruct[0], datestruct[1], datestruct[2])

        isocal_week = int(date.isocalendar()[1])
        formatted_week = int(date.strftime("%W"))

        # week number by "%W" is zero when a new year has occoured 
        # within the week and the weekday is in January. That won't
        # do any good to comparison betweeen isocalendar().
        #
        # here we make sure the week is not zero by asking for the 
        # weeknumber from Monday the same week.
        if formatted_week == 0:
            before_monday = date.isocalendar()[2] - 1
            monday = date - timedelta(days=before_monday)
            formatted_week = int(monday.strftime("%W"))

        # for years beginning on a Monday, all is fine since
        # the "week label" (the one PEOPLE use) and the calculated
        # week is the same.
        if isocal_week == formatted_week:
            return date.date()

        # for the rest, turn the clock backwards since we are 1 week
        # ahead of time.
        behave = timedelta(days=7)
        return (datetime(datestruct[0], datestruct[1], datestruct[2]) - behave).date()


def get_current_site_from_request(request):
    if request.META and "HTTP_HOST" in request.META:
        request_domain = request.META["HTTP_HOST"]
    else:
        return None

    try:
        site = CustomerSite.objects.get(domain=request_domain)
    except ObjectDoesNotExist:
        site = None

    return site

def create_invitation_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))


def records_to_dict(records):
    d = []
    for r in records:
        billable = "no"

        if r.project.billable: billable = "yes"

        d.append({
            "note": r.note,
            "done_at": r.done_at.strftime("%Y-%m-%d"),
            "minutes": r.duration,
            "project": r.project.name,
            "billable": billable
        })
    return d
