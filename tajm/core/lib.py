import re
from datetime import datetime, timedelta
from time import strptime


class TimeUtil:
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
        minutes += int(hhmm[1])

        return minutes

    @staticmethod
    def hhmm(minutes):
        ''' transforms minutes to a timestamp string (HH:MM) '''
        hh = (minutes - (minutes % 60)) / 60
        mm = minutes % 60
        return "%d:%02d" % (hh, mm)

    @staticmethod
    def week_start_end(year, week):
        week_started = TimeUtil.ywd_to_date(year, week, 1)
        week_ended = week_started + timedelta(days=6)

        return week_started, week_ended

    @staticmethod
    def period(year, week):
        ''' Return a readable date period. '''
        # get starting date and ending date of week
        trimmer_a = re.compile('([^\d])0(\d) ')
        trimmer_b = re.compile('^0(\d) ')

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
        the_magic_day = 5

        future = (TimeUtil.ywd_to_date(year, week, the_magic_day) + timedelta(days=7 * diff))

        future_yw = future.isocalendar()

        return future_yw[0], future_yw[1]

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

    @staticmethod
    def num_name_date(year, week):
        weekdays = []

        for i in range(1,8):
            date = TimeUtil.ywd_to_date(year, week, i)
            weekdays.append((i, date))

        return weekdays
