from datetime import datetime, timedelta
import re
from time import strptime
from django.utils.translation import ugettext

the_magic_day = 5
trimmer_a = re.compile('([^\d])0(\d) ')
trimmer_b = re.compile('^0(\d) ')

days = [u"Sön", u"Mån", u"Tis",
        u"Ons", u"Tor", u"Fre",
        u'Lör', u"Sön"]

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